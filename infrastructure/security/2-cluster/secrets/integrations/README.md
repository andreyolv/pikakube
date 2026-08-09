[← Secrets](../README.md)

# Secret integrations

A store holding a credential is useless until the value reaches a container. These are the three
ways it gets there, and they differ in one thing that matters: whether a Kubernetes `Secret` ends up
existing.

Tools: [`external-secrets/`](external-secrets/README.md) — syncs the store into a `Secret` ·
[`secrets-store-csi-driver/`](secrets-store-csi-driver/README.md) — mounts it as files ·
[`argocd-vault-plugin/`](argocd-vault-plugin/README.md) — substitutes placeholders at render time

## Contents

1. [The three mechanisms](#1-the-three-mechanisms)
2. [The Kubernetes Secret question](#2-the-kubernetes-secret-question)
   - [Why syncSecret gives the advantage back](#why-syncsecret-gives-the-advantage-back)
3. [Refresh and rotation](#3-refresh-and-rotation)
   - [The application still has to notice](#the-application-still-has-to-notice)
4. [Failure modes](#4-failure-modes)
5. [Authentication to the store](#5-authentication-to-the-store)
6. [Anti-patterns](#6-anti-patterns)
7. [How this applies to pikakube](#7-how-this-applies-to-pikakube)

---

## 1. The three mechanisms

| | external-secrets | secrets-store-csi-driver | argocd-vault-plugin |
|---|---|---|---|
| Shape | an operator with CRDs | a CSI driver plus per-provider plugins | a config management plugin for Argo CD |
| When it runs | continuously, on a refresh interval | at pod mount time | at manifest render time |
| Result | a Kubernetes `Secret` | files in a volume, inside the pod | a rendered manifest with values inlined |
| Works with | anything that consumes a `Secret` | apps that read files | Argo CD only |
| GitOps engine | any | any | Argo CD |
| Rotation | re-syncs on the interval | polls, with `enableSecretRotation` | only on the next sync |
| Kubernetes `Secret` created | yes | no, unless `syncSecret` is on | yes, whatever the manifest declared |

**external-secrets** is the most popular by a wide margin, and the reason is compatibility: an
`ExternalSecret` produces an ordinary `Secret`, so every chart, operator, `secretKeyRef` and
`imagePullSecrets` field in the ecosystem keeps working unchanged. It supports a long list of
providers behind one CRD, which also makes it the migration path between stores.

**secrets-store-csi-driver** is a Kubernetes SIG project. The pod declares a CSI volume referencing
a `SecretProviderClass`, and the driver fetches from the store and materialises files under a mount
path. The value only exists inside that pod's mount namespace.

**argocd-vault-plugin** works differently from both: it is a text substitution step. Manifests carry
placeholders (`<path:secret/data/foo#bar>` or an `avp.kubernetes.io/path` annotation), and the
plugin replaces them while Argo CD renders the application. The `discover.find` command in
`argocd-vault-plugin/cmp-plugin.yaml` shows this literally — it greps the manifests for `<path` or
`avp.kubernetes.io` to decide whether the plugin applies.

## 2. The Kubernetes Secret question

Once a value is in a Kubernetes `Secret`, it is exposed the way every Secret is exposed: base64 in
etcd, readable by anyone with `get secrets` in that namespace, visible in an etcd backup.

So the CSI driver's real selling point is not convenience — it is that **no Secret object is
created**. The credential exists as a file inside one pod. Someone with `get secrets` in the
namespace gets nothing; they would need `exec` into that specific pod.

That is a meaningful reduction in blast radius, and it is the only structural security difference
between the three mechanisms.

### Why syncSecret gives the advantage back

The reason most CSI driver deployments do not keep that advantage: too much of Kubernetes consumes
secrets *by reference* rather than by file.

- `imagePullSecrets` needs a `Secret`.
- An Ingress TLS certificate needs a `Secret`.
- Most operators and most Helm charts expect `secretKeyRef` or an existing `Secret` name.
- Anything that is not a pod you control cannot mount a volume.

So the driver ships a `syncSecret` option that creates a mirror `Secret` alongside the mount — and
in this repo it is on (`secrets-store-csi-driver/helm/helmrelease.yaml`, `syncSecret.enabled: true`).
At that point you have the CSI driver's operational complexity *and* a Kubernetes Secret, which is
what external-secrets would have given you more simply.

The rule: enable `syncSecret` per workload where it is genuinely required, not globally. If it is
required globally, use external-secrets instead.

There is a second, non-security reason to want the file form: some applications only accept a file
path (JKS truststores, kubeconfigs, service-account JSON), and mounting is more natural than
projecting a Secret key into a file.

## 3. Refresh and rotation

| Mechanism | How a new value arrives |
|---|---|
| external-secrets | the controller re-reads on `refreshInterval` and updates the `Secret` |
| secrets-store-csi-driver | with `enableSecretRotation: true`, polls every `rotationPollInterval` and rewrites the file |
| argocd-vault-plugin | only when Argo CD re-renders — a sync, not a schedule |

The third row is the important limitation of argocd-vault-plugin: rotation is not automatic. The
value is baked into the rendered manifest, so until something triggers a sync, the cluster keeps the
old credential. That is fine for values that change rarely and wrong for anything on a short TTL.

In this repo the CSI driver is configured with `enableSecretRotation: true` and
`rotationPollInterval: 10s`. Ten seconds is aggressive — it is one request to the store per mounted
secret per ten seconds, per pod. Fine for a demo, a load generator against Vault in production.

### The application still has to notice

Every mechanism here stops at "the new value is available". None of them make the application read
it:

| Consumption | Does the app see the new value? |
|---|---|
| Environment variable from `secretKeyRef` | **no** — env vars are set at container start and never change |
| Volume-mounted `Secret` | the file is updated by the kubelet, but only if the app re-reads it |
| CSI mount | the file is updated on rotation, same caveat |

The env var case is the one that silently defeats rotation, and it is the most common way secrets
are consumed. The fix is a restart, and the Kyverno examples in this repo do exactly that:
`policies/kyverno/examples/restart-deployment-on-secret-change.yaml` and
`refresh-env-var-in-pods.yaml` react to a Secret changing by rolling the Deployment. Reloader-style
controllers solve the same problem.

Rotation without a reload strategy is rotation that only takes effect at the next unrelated deploy.

## 4. Failure modes

What happens when the store is unavailable differs sharply, and this decides whether the store is on
the critical path of pod startup:

| Mechanism | Store unreachable |
|---|---|
| external-secrets | existing `Secret` objects remain; pods start normally; the `ExternalSecret` reports `SecretSyncedError` and values go stale |
| secrets-store-csi-driver | the volume cannot mount, so **the pod does not start** — `FailedMount` |
| argocd-vault-plugin | the Argo CD sync fails; running workloads are untouched |

external-secrets degrades gracefully — stale is better than down. The CSI driver fails closed, which
is arguably more correct security-wise and much worse for availability: a Vault that has resealed
after a restart means every new pod that mounts a secret is stuck.

This is the practical argument for external-secrets in a platform where deployments must proceed
even when the store is having a bad day.

## 5. Authentication to the store

Whatever the mechanism, something must prove its identity to the store. The options are the ones in
[`../stores/`](../stores/README.md#3-authentication-how-a-pod-proves-who-it-is), and the choice
shows up directly in this folder:

- `external-secrets/hashicorp-vault/clustersecretstore.yaml` uses `tokenSecretRef` — a Vault token
  stored in a Kubernetes Secret. It works immediately and it is a static credential in a Secret,
  which is the thing the store was meant to remove.
- `external-secrets/azure-key-vault/clustersecretstore.yaml` uses a service principal client ID and
  secret, again from a Kubernetes Secret. Azure workload identity would remove both.
- `secrets-store-csi-driver/example/` uses Vault's **Kubernetes auth method**, binding a role to
  `bound_service_account_names=secret-sa` in a specific namespace. That is the version with no
  stored credential at all, and it is the pattern to copy.

`ClusterSecretStore` vs `SecretStore` is a related decision: cluster-scoped is convenient and means
one authentication path shared by every namespace. Namespace-scoped stores are more work and let
each tenant authenticate as itself. For a multi-tenant cluster, the cluster-scoped shortcut is how a
namespace ends up able to read another namespace's secrets.

## 6. Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| CSI driver with `syncSecret` on globally | you pay CSI complexity and still create Secrets — the advantage is gone | enable per workload, or use external-secrets |
| Token auth in a `ClusterSecretStore` | a static long-lived credential in a Kubernetes Secret | Kubernetes auth / workload identity |
| One `ClusterSecretStore` for every namespace and tenant | any namespace can pull any path the store's identity can read | namespace-scoped stores, or narrow policies per path |
| Rotation with no reload mechanism | env vars never change; the app keeps the old credential until an unrelated deploy | a restart-on-change policy, or read the file at runtime |
| Very short poll intervals | a request to the store per secret per pod per interval | seconds are for demos; minutes are for production |
| argocd-vault-plugin for short-TTL credentials | the value is frozen into the rendered manifest until the next sync | external-secrets, or a store integration with a refresh loop |
| Assuming the CSI driver degrades gracefully | it fails the mount, so pods will not start when the store is down | know which failure mode you signed up for |
| The `ExternalSecret` template copying everything | `dataFrom` on a whole path pulls in secrets the workload does not need | list the keys explicitly |
| No monitoring on sync status | a failed sync is silent, and the cluster runs on a stale credential indefinitely | alert on `SecretSyncedError` and on mount failures |

## 7. How this applies to pikakube

**external-secrets is the one that is actually integrated.** It has a `kustomization.yaml`
(namespace, HelmRepository, HelmRelease), and two working `ClusterSecretStore` configurations that
its notes record as done: Vault's KV engine at `http://vault.vault:8200` with `path: pikakube`, and
Azure Key Vault via a service principal. That makes it the delivery mechanism for the Vault
deployment in [`../stores/vault/`](../stores/vault/README.md).

Both of those stores authenticate with a stored credential, which is the first thing to improve:
Vault's Kubernetes auth method is already demonstrated in the CSI driver's example folder, and Azure
workload identity would remove the service principal entirely.

The secrets-store-csi-driver folder is a complete worked tutorial against Vault — enable the
Kubernetes auth method, write a read-only policy, bind a role to a ServiceAccount, mount, and
`cat /mnt/secrets-store/my-password`. It is the best explanation of the store-authentication problem
in the repository. Its HelmRelease, however, sets `syncSecret.enabled: true` with a ten-second
rotation poll, which is a demo configuration rather than a deployment one.

argocd-vault-plugin is the odd one out and worth being explicit about: this platform delivers with
**Flux**, not Argo CD, so the plugin has nothing to plug into here. Keep it as a reference for what
the Argo CD approach looks like, and do not expect it to run.

The missing piece across all of this is the reload story. The Kyverno examples folder already
contains policies that restart Deployments when a Secret or a mounted volume changes — those are
the other half of any rotation strategy adopted here.

---

[← Secrets](../README.md)
