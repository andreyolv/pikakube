[← Falco operator](../README.md)

# k8saudit-eks

<https://github.com/falcosecurity/plugins/tree/main/plugins/k8saudit-eks>

The Kubernetes audit log as a Falco event source, on EKS — where you cannot reach the API server's
audit webhook, so you read the log out of CloudWatch instead.

---

## The problem it solves

Everything else in [`../../`](../../README.md) watches the **workload**: syscalls, files, sockets,
process trees. None of it sees the *control plane*. A `kubectl exec` into a production pod, a
ServiceAccount token created for a namespace it has no business in, a Role granting `secrets/get`
cluster-wide, an `anonymous` request that succeeded — those are API server events, and the API
server records them in the audit log.

The stock [`k8saudit`](https://github.com/falcosecurity/plugins/tree/main/plugins/k8saudit) plugin
takes that log directly: Falco opens an HTTP endpoint and the API server's audit *webhook* posts to
it. That requires editing the API server's `--audit-webhook-config-file`, which on EKS you do not
control. AWS closes the gap on its own terms: enable control plane logging and audit events land in
a CloudWatch log group, `/aws/eks/<cluster>/cluster`.

`k8saudit-eks` is the adapter. It polls that log group, reconstructs the audit events, and feeds
them to Falco as the same `k8s_audit` source the standard k8saudit ruleset already targets — so the
rules are unchanged, only the transport differs.

| | k8saudit | k8saudit-eks |
|---|---|---|
| Transport | API server pushes over a webhook | plugin polls CloudWatch Logs |
| Requires | control of the API server flags | EKS control plane audit logging enabled |
| Latency | immediate | `polling_interval` + `shift`, seconds to tens of seconds |
| Credentials | none | AWS, read on the log group |
| Rules | `falcosecurity/plugins/ruleset/k8saudit` | the same ruleset |

## What is here

| File | What it is |
|---|---|
| `namespace.yaml` | `falco-k8saudit-eks` — a namespace of its own, and the reason is below |
| `falco.yaml` | a `Falco` instance, `type: Deployment`, one replica, `nodriver` engine |
| `plugin.yaml` | the `k8saudit-eks` plugin and the `json` plugin it needs |
| `rulesfile.yaml` | the upstream k8saudit ruleset |
| `config.yaml` | output settings |
| `serviceaccount.yaml` | the IRSA annotation — **not needed** under Pod Identity |
| `iam-policy.json` | the AWS permissions the plugin needs |

Nothing declares `load_plugins`. The artifact operator writes both the `plugins:` entry and the
`load_plugins` list into Falco's config from the `Plugin` objects, which is the point of using the
operator for this.

## Why a separate namespace

This is the load-bearing decision in the folder, and it is not cosmetic.

Artifacts scope by **namespace**, not by Falco instance. The artifact operator runs as a sidecar in
each Falco pod, and it watches `Plugin`, `Rulesfile` and `Config` objects **in its own namespace**
only. The `selector` field on those objects filters by *node* labels, not by which `Falco` CR they
belong to.

So if a syscall DaemonSet and this plugin instance shared a namespace, every DaemonSet pod would
also load `k8saudit-eks` — each one polling the same CloudWatch log group, each one alerting on the
same audit events, multiplied by the node count. A node selector cannot separate them, because the
Deployment pod runs on a node the DaemonSet also covers.

One namespace per Falco instance is the only boundary the operator actually offers. The syscall
Falco stays in `falco` with its own artifacts; this one lives alone in `falco-k8saudit-eks`.

## AWS side

Two things have to exist before any of this reports an event.

**1. Control plane audit logging, enabled on the cluster.** Without it the log group is never
created and the plugin polls nothing, silently.

```sh
aws eks update-cluster-config \
  --name your-eks-cluster \
  --logging '{"clusterLogging":[{"types":["audit"],"enabled":true}]}'
```

This is billed: audit logs on a busy cluster are a real CloudWatch ingestion line item, and it is
the cost people discover after the fact rather than before. Set a retention policy on the log group.

**2. An IAM role the pod can assume,** with `iam-policy.json` attached. Substitute `REGION`,
`ACCOUNT_ID` and `CLUSTER_NAME`; the resource is scoped to the one log group, which is the whole
permission the plugin needs.

Then bind it, by either mechanism:

- **EKS Pod Identity** (what
  [`docs/security/workload-identity.md`](../../../../../../docs/security/workload-identity.md)
  standardises on): create an association for namespace `falco-k8saudit-eks`, service account
  `k8saudit-eks`. Nothing changes in this folder — delete `serviceaccount.yaml`.
- **IRSA**: apply `serviceaccount.yaml` with the role ARN filled in. Read the comment in that file
  first — the ServiceAccount is created by the operator and carries RBAC the sidecar depends on, so
  the object there adds an annotation and nothing else.

## Configuration worth understanding

`plugin.yaml` sets four values that are not obvious:

| Field | Set to | Why |
|---|---|---|
| `openParams` | the cluster name | not a URL — the plugin derives the log group from it |
| `polling_interval` | `10` | seconds between CloudWatch reads; lower means more API calls and more cost |
| `shift` | `10` | how far back each poll reaches. CloudWatch delivery is not instant, and a `shift` shorter than the delivery lag drops events on the floor without an error |
| `use_async` | `false` | upstream's own recommendation for this plugin; the async extraction path is an optimisation, not a default worth inheriting here |

`profile` is deliberately absent. Upstream's example sets `profile: "default"`, which is right on a
laptop and wrong in a pod — under Pod Identity or IRSA the credentials arrive through the
environment, and naming a profile sends the SDK looking for a file that is not there.

## Limitations to accept before relying on it

- **CloudWatch truncates log lines over 10,000 characters**, and a truncated line cannot be parsed.
  Large audit events — a big ConfigMap write, a verbose admission response — are simply lost. This
  is a property of the transport, not a bug in the plugin, and there is no setting that fixes it.
  Audit-log detection on EKS is therefore *lossy by construction*, which is worth knowing before
  anyone treats it as a compliance control.
- **One replica, always.** A second pod polls the same log group and duplicates every alert. The
  Deployment uses `strategy: Recreate` so that even a rollout does not briefly run two.
- **Polling is not streaming.** Detection lands seconds to tens of seconds after the event, and the
  event itself describes something that already succeeded. Audit events are past tense —
  [§3](../../README.md#3-detection-vs-enforcement) applies with extra force here, because unlike a
  syscall there was never a point at which this could have been blocked. Admission control
  ([`../../../policies/`](../../../policies/README.md)) is the layer that says no; this one says
  what happened.
- **Rules are still the job.** The upstream k8saudit ruleset alerts on `kubectl exec`, on
  privileged pod creation, on ServiceAccount and RBAC changes — all of which your CI, your
  operators and your platform controllers do routinely. Untuned, this is a firehose of your own
  automation. [§4](../../README.md#4-the-alert-volume-problem) is the relevant reading, and the
  operator's `Rulesfile` objects are what make the tuning cheap.
- **Cluster-specific by design.** `openParams` names one cluster. A second EKS cluster means a
  second instance and a second namespace, not a second entry in a list.

## Notes

**Artifacts are pinned by tag, not digest.** `0.6.0`, `0.7.3` and `0.10.1` are version tags, which
is stricter than the `latest` used in [`../artifacts/`](../artifacts/) and looser than the digest
pinning the parent README argues for. The `Plugin` and `Rulesfile` CRDs accept a digest in the same
`tag` field — `tag: sha256:...` — and for strict GitOps that is the correct value, because the
operator only re-pulls when the spec changes: a mutable tag whose content moves on the registry is
not noticed until the pod restarts. The tradeoff is that Renovate in this repository only manages
`ocirepository.yaml` files, so these digests would be updated by hand.

**The ruleset is code fetched at reconcile time.** It is pulled from `ghcr.io` and executed as
detection logic, with the caveat the parent README already states: a wrong rules file does not open
a hole, it closes an eye.

**Falco ≥ 0.35.0** is required by the plugin. The `Falco` CR leaves `version` unset, so the operator
deploys the current upstream release, which satisfies this — pin `spec.version` if you would rather
the Falco version not move on its own.

**This is not wired into `clusters/dev/`,** like the rest of `../`. It is also the one deployment in
this folder that cannot run on the kind clusters in [`clusters/kind-configs/`](../../../../../../clusters/kind-configs/),
since it needs a real EKS control plane and real AWS credentials. On kind, the plugin to use is
plain `k8saudit` with the audit webhook; `clusters/kind-configs/audit-logs.yaml` already turns
auditing on for a kind control plane, though it writes to a file rather than posting to a webhook,
so the API server flags still need extending.

---

[← Falco operator](../README.md)
