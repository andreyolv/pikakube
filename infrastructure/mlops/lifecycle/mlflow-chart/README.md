[← Lifecycle](../README.md)

# MLflow (Helm chart)

<https://github.com/mlflow/mlflow>
<https://github.com/mlflow/mlflow/tree/master/charts>
<https://github.com/cloudnative-pg/cloudnative-pg>
<https://github.com/external-secrets/external-secrets>

---

## The problem it solves

Same tool as [`../mlflow/`](../mlflow/README.md) — MLflow tracking and the Model Registry. What
this folder solves is different: it is the **rebuild**, and for a long time it meant rewriting
manifests, because MLflow shipped no Helm chart and improving a deployment could not be a version
bump.

That premise expired. MLflow published an **official Helm chart** as an OCI artifact in July 2026,
and this folder consumes it — hence the name. There is no hand-written `deployment.yaml`,
`service.yaml` or `serviceaccount.yaml`; what is here is the chart reference, its values, and the
parts the chart does not cover.

The problems this rebuild fixes, each of which was a real weakness of the first deployment:

| Problem in `mlflow/` | Fix here |
|---|---|
| Third-party image on a floating `:latest` tag | the chart's official `ghcr.io/mlflow/mlflow` image, pinned by chart digest |
| Postgres as a hand-written Deployment + PVC — no backups, no failover, no metrics | a CloudNativePG `Cluster` with a `PodMonitor` |
| Credentials in a committed `Secret` template, injected by hand | a generated 42-character password through `external-secrets` |
| Static MinIO access keys in a Secret | a ServiceAccount annotated with an IAM role — no long-lived keys (see the note on MinIO below) |
| No metrics from the server | `metrics.enabled` on the chart, with the `ServiceMonitor` waiting on a Prometheus Operator — see the notes |
| Every change is a manifest rewrite | a values file against a versioned chart |

### What is deployed here

| File | What it contains |
|---|---|
| `namespace.yaml` | the `mlflow` namespace, labelled `agentpool: spot` |
| `helm/ocirepository.yaml` | the chart source: `oci://ghcr.io/mlflow/charts/mlflow`, tag `0.1.0` pinned to its digest, `layerSelector` set to the Helm chart layer |
| `helm/helmrelease.yaml` | the values — backend store, artifact root, S3 endpoint, metrics, IRSA annotation |
| `minio/` | an in-cluster S3 stand-in so the artifact path can actually be exercised — chart, credentials and the `mlflow` bucket ([README](minio/README.md)) |
| `postgres/cluster.yaml` | a CloudNativePG `Cluster`: 1 instance, PostgreSQL 17.5, 2 Gi storage, database and owner both `mlflow` |
| `postgres/podmonitor.yaml` | a hand-written `PodMonitor` selecting `cnpg.io/cluster: postgres` — CNPG deprecated `spec.monitoring.enablePodMonitor`, so the object is owned here |
| `postgres/password.yaml` | an external-secrets `Password` generator — 42 characters, 5 digits, no symbols |
| `postgres/externalsecret.yaml` | an `ExternalSecret` that draws from that generator and **owns** the `mlflow-app` Secret: `username`, `password` and a full `connection` string |

The server reads the connection string from the `connection` key of `mlflow-app` — the chart
turns `mlflow.backendStoreUriFrom` into `MLFLOW_BACKEND_STORE_URI` — and artifacts go to
`s3://mlflow/` with `MLFLOW_S3_ENDPOINT_URL` pointing at [`minio/`](minio/README.md). That is the
Postgres + object-storage pairing argued for in
[`../README.md`](../README.md#4-the-backing-store-decision), with both halves runnable on a local
cluster.

**Who owns the password** is the part worth reading twice, because the obvious arrangement does
not work. The direction is: external-secrets generates it, CloudNativePG consumes it.

- `creationPolicy: Owner` on `mlflow-app` — external-secrets creates the Secret outright. It never
  waits for another controller, so there is nothing to race.
- `type: kubernetes.io/basic-auth` with `username` and `password` — the shape CloudNativePG
  requires of any Secret it takes a password from.
- `bootstrap.initdb.secret.name: mlflow-app` on the `Cluster` — the app role is created *with* the
  generated password rather than one the operator invents.
- `managed.roles` with `passwordSecret: mlflow-app` — and keeps it. Bootstrap only fires once;
  this is what applies every later refresh of the generator to the role.
- `cnpg.io/reload: "true"` — the label that tells CloudNativePG to watch the Secret.
- `refreshInterval: 168h` — one week. With a generator source this is a rotation cadence, not a
  sync cadence.

**The arrangement this replaced was the natural one, and it deadlocks.** Pointing an
`ExternalSecret` at CloudNativePG's own `postgres-app` with `creationPolicy: Merge` reads
correctly — let the operator own its Secret, merge one key into it. In practice external-secrets
reconciles before the cluster has bootstrapped, finds no Secret to merge into, and reports
`SecretMissing`. `refreshInterval` is also the retry interval, so at `168h` the key that MLflow
boots from does not appear for a week, and the server crash-loops on
`couldn't find key connection in Secret mlflow/postgres-app` the entire time. Inverting the
ownership removes the ordering problem instead of timing around it.

Note also that `mlflow-app` and CloudNativePG's `postgres-app` both exist, and **`mlflow-app` is
the one to read.** After a rotation, `postgres-app` still holds the password from bootstrap.

## When to use it

- Use this rather than [`../mlflow/`](../mlflow/README.md) for any new deployment. It is the same
  tool, correctly assembled.
- Where a Postgres operator is already available — CloudNativePG gives backups, failover and
  metrics that a hand-written Deployment does not, at roughly no extra effort.
- On a cloud where workload identity exists (IRSA here). Removing static object-storage keys is
  the single largest security improvement over the first deployment.
- Where Prometheus is scraping — the chart's `ServiceMonitor` and the CNPG `PodMonitor` are both
  a value away, so the server and its database become visible without extra work.

## When not to use it

- **As-is, on an exposed endpoint.** There is no authentication in this folder. See the notes.
- On a cluster without the CloudNativePG operator and external-secrets installed — the
  `postgres/` manifests are inert CRDs without them, and the server will not start without the
  Secret they produce.
- Expecting the metrics to arrive on their own. The Prometheus Operator is not installed on this
  cluster, which is why `serviceMonitor` is commented out — see the notes.
- Outside AWS without changing the `serviceAccount.annotations` values. The IRSA annotation is
  AWS-specific; the equivalents are Workload Identity on GCP and Azure Workload Identity.
- Alongside [`../mlflow/`](../mlflow/README.md). Both claim the `mlflow` namespace. They are
  alternatives, not a pair.

## Notes

**The chart is version 0.1.0.** Official, published by the MLflow project on every release, and
new — first tag, July 2026. It is a single-Deployment chart with no database or object-store
dependencies of its own, which is exactly the right scope: the pieces this folder already solved
well stay where they are. Being 0.x, expect values to move between releases; the digest pin means
that happens on a reviewed pull request rather than silently.

**Moving to the chart is an MLflow upgrade.** The earlier hand-written Deployment pinned `v3.3.2`;
chart `0.1.0` has an `appVersion` of `3.14.0` and resolves the image to `v3.14.0-full`. MLflow runs
schema migrations against the backend store on start-up, so the repository's own anti-pattern
table applies here: **back up Postgres before the first reconcile**. CNPG makes that cheap and it
is not automatic.

**Object names come from the chart.** With no `fullnameOverride`, the release is `mlflow` and the
chart is `mlflow`, so the Deployment, Service and ServiceAccount are all `mlflow-mlflow` and the
server answers on `mlflow-mlflow.mlflow.svc.cluster.local:5000`. Anything still pointing at the
old `mlflow-server` name needs updating, or `fullnameOverride: mlflow-server` needs setting.

**The metrics gap is not closed yet, and it is blocked on something else.** `metrics.enabled` is
on, so the server serves Prometheus metrics. `serviceMonitor` is commented out and
`postgres/podmonitor.yaml` cannot be applied, for the same reason:

```
$ kubectl get crd podmonitors.monitoring.coreos.com
Error from server (NotFound)
```

There is no Prometheus Operator on this cluster — the
[kube-prometheus-stack `HelmRelease`](../../../observability/metrics/storage/prometheus/kube-prometheus-stack/helm/helmrelease.yaml)
is commented out in full. Both objects are correct and both are waiting on that. One detail for
when it lands: `metrics.path` is read by the chart's ServiceMonitor template but absent from its
`values.yaml`, so it is worth setting explicitly rather than relying on the empty default.

**`--allowed-hosts` is not optional on MLflow 3.** The server ships DNS-rebinding protection that
rejects any `Host` header it does not recognise, and the default list is localhost plus private
IPs — which does not include the cluster DNS name. Without it every in-cluster client gets:

```
API request to endpoint /api/2.0/mlflow/experiments/get-by-name failed with error code 403 != 200.
Response body: 'Invalid Host header - possible DNS rebinding attack detected'
```

The server starts, the health probe passes and the pod reads `1/1 Running`, because `/health` is
reached over the pod IP. Only real clients fail. `server.value_options.allowed_hosts` covers
`mlflow-mlflow*` for in-cluster names and `localhost*` for a port-forward; an ingress hostname has
to be added to that list too.

**No authentication, and this is the significant gap.** [`../mlflow/`](../mlflow/README.md) put an
`oauth2_proxy` in front of the UI, restricted to a GitHub org and team. That is gone here. MLflow's
open-source UI has no built-in authentication of its own, and it holds every logged metric,
parameter, dataset sample and model artifact. Whatever fronts this deployment — an ingress with an
auth annotation, an auth proxy, a service mesh — has to supply it, and it is not in this folder.
The pattern lives under
`../../../security/2-cluster/identity-access/authentication/auth-proxy/`.

**The `agentpool: spot` label on the namespace.** A hint that workloads here are expected to land
on spot/preemptible nodes. A namespace label does nothing by itself — it only has an effect if a
mutating policy, a scheduler plugin or a cloud add-on reads it. Worth being deliberate about:
MLflow's server tolerates eviction reasonably (it is stateless, and `deploymentStrategy: Recreate`
handles the restart), but a single-instance CloudNativePG cluster on spot capacity means the
tracking database goes away with the node.

**Artifacts now point at MinIO, and that overrides IRSA.** `MLFLOW_S3_ENDPOINT_URL` resolves to
`minio.mlflow.svc.cluster.local:9000` and the access keys come from the `minio-credentials`
Secret. boto3 resolves environment credentials before the web-identity token, so the
`eks.amazonaws.com/role-arn` annotation does nothing while those variables are set. Both are
present deliberately: the annotation records the production intent, the `env` block makes the
artifact path testable today. **Moving to real S3 is deleting the `env` block**, not editing the
annotation — and the role ARN there is still a placeholder.

This is a deliberate step back from the first deployment on one axis. `mlflow/` used static MinIO
keys and that was listed above as a weakness; the difference is that those were the only credential
path it had, while here they are a local stand-in sitting in front of a role-based one that is one
deletion away. Worth being honest that the committed `pikakube` / `pikakube` pair is in the
repository either way.

**One CNPG instance.** `instances: 1` means no failover and no read replica; a node loss is an
outage of tracking and the registry. CNPG still earns its place at one instance — backups,
monitoring and a managed upgrade path — but this is not a highly available database, and the
`agentpool: spot` label above makes that more pointed.

**Storage is 2 Gi**, the same as the first deployment. The backend store grows with the number of
runs logged; this is a starting value, not a sized one.

**Garbage collection is available and off.** The chart ships a `mlflow gc` CronJob behind
`garbageCollection.enabled`. It only removes resources that were already soft-deleted, so it is
safe to enable, and it is the thing that stops the backend store growing forever. Left off here
because nothing has accumulated yet.

**A rotation still needs a pod restart.** `managed.roles` applies a refreshed password to the
Postgres role, and the chart injects the connection string through `secretKeyRef` — an environment
variable, fixed at pod start. So the week the generator rotates, the running server keeps the old
credentials until it is restarted. [Reloader](../../../devops/config-reload/reloader/README.md)
solves exactly this, but its `reloader.stakater.com/auto` annotation belongs on the Deployment and
the chart only exposes `podAnnotations` — so today the restart is manual, or `refreshInterval` goes
to `0` to stop generating a new password at all.

**Why the folder is named `mlflow-chart` rather than replacing `mlflow/`.** The first deployment is
kept as history. That is defensible as a record, and it is a trap for anyone who applies the wrong
directory — both target the same namespace.

---

[← Lifecycle](../README.md)
