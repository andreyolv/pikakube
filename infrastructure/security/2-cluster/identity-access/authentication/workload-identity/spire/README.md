[← Workload identity](../README.md)

# SPIRE

<https://github.com/spiffe/spiffe>
<https://github.com/spiffe/spire>
<https://github.com/spiffe/helm-charts-hardened>

---

## The problem it solves

SPIRE is the reference implementation of **SPIFFE**, and it is the general, vendor-neutral
answer to the question in [`../README.md`](../README.md): how does a workload prove what it is,
without holding a secret?

The mechanism, and the reason it is different in kind from anything else in this folder:

> **A workload asks a local Unix socket "who am I?", presenting no credential at all, and gets
> back a short-lived cryptographic identity.**

The SPIRE agent identifies the caller by inspecting the calling process — its PID, its cgroup,
and therefore its pod, its namespace and its ServiceAccount. Nothing is claimed by the workload;
everything is observed by the platform. A compromised pod cannot ask for a different identity,
because it cannot change what the attestor sees.

| Piece | What it does |
|---|---|
| **SPIRE Server** | the certificate authority for a **trust domain**. Holds registration entries, signs SVIDs, and can federate with other trust domains |
| **SPIRE Agent** | a DaemonSet, one per node. Node-attests itself to the server, then workload-attests the pods on its node |
| **Workload API** | the Unix domain socket the workload calls. No token, no config file, no secret |
| **Registration entry** | the policy: selectors → SPIFFE ID. "ServiceAccount `payments` in namespace `production` is `spiffe://example.org/ns/production/sa/payments`" |
| **SVID** | the issued credential — an X.509 certificate or a JWT, typically valid for an hour, rotated at half-life |

Two things it gives you that a service mesh does not:

- **Identity beyond the cluster.** VMs, CI runners, bare-metal hosts and other clusters can all
  hold SPIFFE identities from the same trust domain, with node attestors for AWS, Azure, GCP,
  TPM and more.
- **Federation between trust domains.** Two organisations, or two clusters run by different
  teams, can exchange trust bundles and authenticate each other's workloads without a shared
  secret or a shared CA.

Prefer **X.509-SVIDs** wherever mTLS is possible: the identity is proved by possessing a private
key, so it cannot be replayed. **JWT-SVIDs** exist for endpoints that only accept a header, and
they are bearer tokens with all that implies — still vastly better than a stored secret, because
they live for minutes.

## When to use it

- **Service-to-service identity across a whole platform**, especially where the platform is not
  only Kubernetes. This is the case SPIFFE was designed for.
- **Multi-cluster or multi-cloud**, where one identity model has to span environments that have
  nothing else in common.
- **Federating trust with another organisation** without exchanging a secret or a CA key.
- **You want an open standard**, not a cloud provider's proprietary identity. SPIFFE IDs are
  portable; an IAM role ARN is not.
- **As the identity provider for a service mesh.** Istio can consume SPIRE directly, which
  extends the mesh's identity to workloads outside it — the composition described in
  [`../README.md`](../README.md) §7.
- **The workload itself needs its identity**, not just the sidecar — to sign something, to
  authenticate to a third system, or to make its own authorization decisions.

## When not to use it

- **The only consumer is one cloud's API.** Cloud federation (IRSA,
  [azure-workload-identity](../azure-workload-identity/README.md), GCP Workload Identity) is
  free, needs no new control plane, and solves that case completely. Deploying SPIRE for it is
  a large amount of infrastructure for something the cloud already does.
- **A service mesh already covers everything.** Istio and Linkerd issue workload identities and
  do mTLS automatically. If nothing outside the mesh needs identity, SPIRE is duplicate
  machinery with its own failure modes.
- **Small or single-cluster environments.** A CA, a server, a datastore, a DaemonSet and a
  registration policy is real operational weight, and the benefit scales with the number of
  environments it unifies.
- **Applications cannot be changed and there is no sidecar.** Using SVIDs directly means calling
  the Workload API, which means either a SPIFFE-aware library, a sidecar such as Envoy, or the
  SPIFFE CSI driver to project SVIDs as files. Plan which of the three before adopting it.
- **You just want certificates in pods.** [autocert](../autocert/README.md) does that with a
  webhook and step-ca, without the SPIFFE model.

Two operational realities worth knowing up front:

- **The SPIRE Server is a certificate authority.** Its key is the root of trust for every
  workload identity in the trust domain. It needs the custody, backup and rotation planning that
  any CA key needs — the reasoning is in
  [`certificates/README.md`](../../../../certificates/README.md).
- **The trust domain name is effectively permanent.** It is embedded in every SPIFFE ID and every
  federation relationship. Changing it later means re-issuing everything and re-establishing
  every federation. Choose a real, stable name — a domain you own — rather than `example.org`.

## Notes

**`https://github.com/spiffe/spiffe`** — the **standard**, not an implementation. Worth reading
separately from SPIRE: it defines the SPIFFE ID format, the SVID formats, the Workload API, and
the federation model. Anything can implement it, and Istio, Linkerd and several commercial
products do. Choosing SPIFFE is choosing a specification; choosing SPIRE is choosing one
implementation of it.

**`https://github.com/spiffe/spire`** — the reference implementation, and a CNCF graduated
project.

**`https://github.com/spiffe/helm-charts-hardened`** — the chart repository the staged manifests
use, and the name is meaningful. The SPIFFE project maintains a *hardened* chart set with
security-conscious defaults — restricted pod security contexts, tighter RBAC, and sensible
production posture — as distinct from the older, more permissive charts. Using this one is the
right choice, and it is worth knowing it exists because the older charts still appear in search
results.

What is staged: a `HelmRepository` named `spire` in `flux-system`, a `Namespace` `spire`, and
**two** HelmReleases, which is the correct pattern:

| Release | Chart | Version | Note |
|---|---|---|---|
| `spire-crds` | `spire-crds` | `0.5.0` | the custom resource definitions, installed first |
| `spire` | `spire` | `0.24.0` | the server, the agent DaemonSet and the controller manager. Declares `dependsOn: spire-crds` |

The `dependsOn` is the detail worth pointing at: CRDs must exist before the resources that use
them are reconciled, and Flux does not infer that ordering. Splitting CRDs into their own
release and declaring the dependency is the standard fix, and it is done correctly here.

**Both releases have empty `values`** — only the ArtifactHub and upstream `values.yaml` reference
links are recorded as comments. Nothing is configured. In particular there is **no trust
domain**, which is the one setting that must be decided before deploying and is painful to
change afterwards.

Also absent, and needed for a working deployment: registration entries. The modern approach is
the **SPIRE Controller Manager**, which is included in the chart and turns
`ClusterSPIFFEID` custom resources into registration entries automatically — so a workload's
identity is declared next to the workload rather than registered by hand against the server's
API. That is the piece that makes SPIRE operable at all in Kubernetes, and it is worth enabling
deliberately rather than discovering later.

---

[← Workload identity](../README.md)
