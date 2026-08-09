[← Secret integrations](../README.md)

# External Secrets Operator

<https://github.com/external-secrets/external-secrets>

An operator that reads from an external secret store and writes the value into a Kubernetes `Secret`.
One API across Vault, Azure Key Vault, AWS Secrets Manager and dozens of others.

---

## The problem it solves

A secret store holds the credential. A pod needs it. Everything in between is this operator's job.

The alternative is a per-store integration: HashiCorp's Vault Secrets Operator for Vault, Azure's CSI
provider for Key Vault, AWS's for Secrets Manager. Each with its own CRDs, its own conventions, its
own upgrade cycle. Switching stores, or running two, means learning both.

External Secrets Operator puts one API in front of all of them:

| CRD | Role |
|---|---|
| `SecretStore` | how to reach a store, namespaced |
| `ClusterSecretStore` | the same, cluster-wide |
| `ExternalSecret` | which keys to fetch and what `Secret` to produce |
| `ClusterExternalSecret` | an `ExternalSecret` pushed into many namespaces |
| `PushSecret` | the reverse — write a Kubernetes `Secret` **into** the store |

The output is an ordinary `Secret`, and that is the whole reason it is the most popular option in
[`../`](../README.md). Every chart, every operator, every `secretKeyRef`, every `imagePullSecrets`
field keeps working unchanged. Nothing in the ecosystem has to know a store exists.

Three capabilities beyond the basic fetch that matter in practice:

- **Templating.** The `target.template` block builds the `Secret`'s contents from fetched values —
  assembling a connection string from a host, a user and a password, or producing a
  `dockerconfigjson`. Without it, the shape the store holds must match the shape the app wants.
- **`dataFrom`.** Pull every key under a path, or select by regex. Convenient, and see the
  anti-patterns in [`../README.md`](../README.md#6-anti-patterns) — it pulls in secrets the workload
  does not need.
- **Graceful degradation.** If the store is unreachable, existing `Secret` objects stay. Pods keep
  starting; the values go stale and the `ExternalSecret` reports the error. Compare with
  [secrets-store-csi-driver](../secrets-store-csi-driver/README.md), where an unreachable store means
  pods cannot mount and therefore cannot start.

## When to use it

- **Anything consumes the credential by reference.** Charts, operators, `imagePullSecrets`, Ingress
  TLS. If it is not a pod you wrote, it wants a `Secret`.
- **More than one store, or the possibility of one.** Vault today, a cloud store tomorrow, both
  during a migration — one API covers all of it.
- **Deployments must proceed when the store is having a bad day.** Stale beats down.
- **The store's layout does not match what the app wants.** Templating bridges it without changing
  either side.
- **You want the same mechanism in every namespace.** `ClusterExternalSecret` distributes one
  definition across namespaces by selector.
- **Migrating *to* a store.** `PushSecret` writes existing Kubernetes Secrets into the store, which
  turns "move everything to Vault" into a declarative step rather than a scripted one.

## When not to use it

- **You specifically do not want a Kubernetes `Secret` to exist.** That is the one thing it cannot
  avoid — the whole design is to produce one. Anyone with `get secrets` in the namespace has the
  credential. If reducing that blast radius is the goal, the CSI driver is the tool, with the
  caveats in [`../README.md`](../README.md#why-syncsecret-gives-the-advantage-back).
- **Only one store, and its native operator does more.** HashiCorp's
  [Vault Secrets Operator](../../stores/vault/vault-secrets-operator/README.md) understands Vault's
  leases, dynamic secrets and rotation as first-class concepts and can trigger rollouts on rotation.
  ESO is broader; VSO is deeper on Vault.
- **You need the app to see a rotated value without a restart.** ESO updates the `Secret`; whether
  anything notices is a separate problem, and for environment variables the answer is no. See
  [`../README.md`](../README.md#the-application-still-has-to-notice).
- **Store authentication is not sorted out.** A `ClusterSecretStore` authenticating with a static
  token in a Kubernetes Secret has moved the problem, not solved it — see the Notes.
- **A very large number of secrets.** Every `ExternalSecret` polls on its refresh interval. Hundreds
  of them at a short interval is real load on the store.

## Notes

Every original note from `doc.md`, translated and explained, plus the state of this folder.

### Vault integration — done

> DONE
> - Integrated with HashiCorp Vault to fetch credentials from the KV Secret Engine.

`hashicorp-vault/clustersecretstore.yaml`:

```yaml
provider:
  vault:
    server: http://vault.vault:8200
    path: pikakube
    version: v2
    auth:
      tokenSecretRef:
        name: vault-policy-token
        key: token
```

Reading it field by field:

| Field | Meaning |
|---|---|
| `server` | the in-cluster Vault service from [`../../stores/vault/vault/`](../../stores/vault/vault/README.md). Plain HTTP — acceptable inside a cluster with a mesh or on a local setup, and something to fix otherwise |
| `path` | the mount point of the KV engine — `pikakube`, matching the `vault secrets enable -path=...` step in Vault's `init.sh` |
| `version: v2` | KV v2, which is versioned. This changes the API path (`/data/` is inserted), and getting it wrong produces a confusing 404 |
| `auth.tokenSecretRef` | a **static Vault token** held in a Kubernetes Secret |

That last row is the thing to improve. A long-lived token in a `Secret` is exactly the kind of
credential the store was meant to eliminate, and anyone with `get secrets` in `external-secrets` can
read it and then read everything the token's policy allows.

The replacement is Vault's **Kubernetes auth method** — the operator's ServiceAccount token is
verified by Vault against the API server, and no credential is stored anywhere. The worked example
is already in this repository, in
[`../secrets-store-csi-driver/`](../secrets-store-csi-driver/README.md).

`hashicorp-vault/external-secret.yaml` and `vault-token-secret.yaml` complete the example: the
`ExternalSecret` that names the keys to fetch, and the Secret holding the token.

### Azure Key Vault integration — done

> - Integrated with Azure Key Vault to fetch credentials from the KV Secret Engine.

`azure-key-vault/clustersecretstore.yaml` uses the `azurekv` provider with a `tenantId`, a
`vaultUrl`, and a service principal (`clientId` + `clientSecret`) read from a Secret named
`azure-key-vault-spn` in the `external-secrets` namespace.

Same structural issue, one level worse: a service principal client secret is a **cloud** credential
stored in a Kubernetes Secret, and it does not expire on its own. Azure **workload identity** removes
it entirely — the pod's ServiceAccount token is federated to an Azure identity and no secret is
stored. That is the "best secret is one that does not exist" point from
[`../../README.md`](../../README.md#5-the-best-secret-is-one-that-does-not-exist), and this is the
clearest instance of it in the repository.

Note the placeholder values (`tenantId: xxxxxxx`, `my-keyvault`), so this file is a template rather
than live configuration.

### Recorded limitation: webhook provider with bearer token auth

> not: Webhook provider with bearer authentication token
> <https://github.com/external-secrets/external-secrets/issues/3871>

The `webhook` provider lets ESO fetch from any HTTP API that is not one of the supported stores — a
useful escape hatch for an internal secrets service. The recorded finding is that authenticating that
webhook with a **bearer token** did not work as needed, with the upstream issue kept as the evidence.

Recorded as a "not", meaning it was attempted and did not work. Worth re-checking against the
deployed chart version (0.10.2) before assuming it still applies; the webhook provider has changed
since.

The general lesson: the long provider list is ESO's main selling point, and the providers are not
equally mature. The mainstream ones (Vault, AWS, Azure, GCP) are well travelled; the generic escape
hatches are thinner.

### How it is deployed here

This is the most completely wired integration in [`../../`](../../README.md):

| File | Role |
|---|---|
| `kustomization.yaml` | namespace, HelmRepository, HelmRelease — so Flux actually delivers it |
| `helm/helmrelease.yaml` | chart `external-secrets` 0.10.2, `upgrade.crds: CreateReplace` |
| `hashicorp-vault/` | a working `ClusterSecretStore`, `ExternalSecret` and token Secret |
| `azure-key-vault/` | the same three against Azure Key Vault |

`upgrade.crds: CreateReplace` is correct and not optional: the CRDs *are* the interface, Helm does
not upgrade them by itself, and a stale CRD means new fields silently do nothing.

Note that the kustomization delivers the operator only. The `ClusterSecretStore` and `ExternalSecret`
examples in the two provider folders are not in it — they are references, applied by hand.

The gap worth closing first is authentication: both stores use a stored credential, and both have a
credential-free alternative available (Vault Kubernetes auth, Azure workload identity).

---

[← Secret integrations](../README.md)
