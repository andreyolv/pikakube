[← Vault](../README.md)

# Vault Secrets Operator

<https://developer.hashicorp.com/vault/tutorials/kubernetes/vault-secrets-operator>
<https://github.com/hashicorp-education/learn-vault-secrets-operator/tree/main>
<https://github.com/hashicorp/vault-secrets-operator>

HashiCorp's own operator for syncing Vault secrets into Kubernetes `Secret` objects. Their current
recommendation, replacing the agent injector and the CSI provider.

---

## The problem it solves

Vault holds the credential; a pod needs it. HashiCorp shipped three answers over the years and this
is the third — see [`../README.md`](../README.md#2-the-four-ways-to-get-a-vault-secret-into-a-pod)
for the comparison.

The two earlier ones each have a structural cost. The **agent injector** puts a sidecar in every pod,
so secret delivery scales with pod count and the templating lives in annotations. The **CSI
provider** creates no `Secret`, which is a real security advantage and means anything consuming
secrets by reference — `imagePullSecrets`, Ingress TLS, most charts — cannot use it.

The Vault Secrets Operator is a single controller with CRDs:

| CRD | Role |
|---|---|
| `VaultConnection` | where Vault is |
| `VaultAuth` | how to authenticate — Kubernetes, JWT, AppRole |
| `VaultStaticSecret` | sync a KV secret into a `Secret` |
| `VaultDynamicSecret` | request a **dynamic** secret, and renew or rotate the lease |
| `VaultPKISecret` | request a certificate and renew before expiry |

What separates it from the vendor-neutral [external-secrets](../../../integrations/external-secrets/README.md):
it understands Vault's own concepts. Leases, renewal, revocation and dynamic secrets are
first-class rather than approximated by a polling interval.

The capability that follows from that, and is the strongest reason to choose it:
`rolloutRestartTargets`. When a secret rotates, the operator can trigger a rolling restart of the
named Deployments or StatefulSets. That closes the gap described in
[`../../../integrations/README.md`](../../../integrations/README.md#the-application-still-has-to-notice)
— rotation is pointless if the consumer reads environment variables set at container start and never
looks again.

It also supports client-side caching with encrypted persistence, so the operator does not have to
re-authenticate to Vault on every restart.

## When to use it

- **Vault is the only store, and will stay that way.** Then the deeper integration beats the broader
  abstraction.
- **You are using dynamic secrets.** `VaultDynamicSecret` handles lease renewal and rotation
  properly. external-secrets treats a dynamic secret as a value to poll for, which is not the same
  thing and generates a new lease each time.
- **Rotation must actually take effect.** `rolloutRestartTargets` is the piece nothing else here
  provides.
- **You need certificates from Vault's PKI engine.** `VaultPKISecret` renews before expiry.
- **You want HashiCorp support.** It is theirs, released with Vault, and covered by an enterprise
  support contract if you have one.
- **Migrating off the agent injector.** No sidecars, no annotation templating, one controller.

## When not to use it

- **More than one store, now or later.** external-secrets speaks Vault, Azure Key Vault, AWS Secrets
  Manager and dozens of others through one API. Two stores with VSO means two integrations.
  Azure Key Vault is already in use in this repository — see
  [`../../../integrations/external-secrets/`](../../../integrations/external-secrets/README.md).
- **external-secrets is already deployed against the same Vault.** Two controllers writing the same
  `Secret` is two sources of truth and a fight. Pick one — and see the Notes, because that is the
  situation here.
- **You do not want a Kubernetes `Secret` to exist.** It produces one, by design. That is the CSI
  driver's job, with the caveats in
  [`../../../integrations/README.md`](../../../integrations/README.md#why-syncsecret-gives-the-advantage-back).
- **Vault is not highly available.** The operator depends on Vault being reachable; a sealed Vault
  means stale secrets and failing syncs.
- **The licence matters.** It is HashiCorp software under the BSL, like Vault itself.
  [OpenBao](../../openbao/README.md) users need a different path.

## Notes

Every original note from `doc.md`, translated and explained, plus the state of this folder.

### The official tutorial

> <https://developer.hashicorp.com/vault/tutorials/kubernetes/vault-secrets-operator>

HashiCorp's walkthrough: install the operator, create a `VaultConnection` and a `VaultAuth` using the
Kubernetes auth method, then a `VaultStaticSecret` that produces a `Secret`, and a
`VaultDynamicSecret` against a database engine.

The part worth reading closely is the auth setup. The Kubernetes auth method binds a Vault role to a
ServiceAccount in a namespace, so the operator authenticates with a token the API server issues and
**nothing is stored**. That is the pattern already demonstrated in
[`../../../integrations/secrets-store-csi-driver/`](../../../integrations/secrets-store-csi-driver/README.md),
and the thing the external-secrets configuration in this repo does not yet do.

### The companion repository

> <https://github.com/hashicorp-education/learn-vault-secrets-operator/tree/main>

The runnable manifests for that tutorial — a Vault configuration, a sample application, and the CRDs
that connect them. More useful than the prose, because the CRD examples show the field layout
directly.

### How it is deployed here

`helm/helmrelease.yaml`, chart `vault-secrets-operator` 0.3.2 into its own namespace:

| Setting | Meaning |
|---|---|
| `dependsOn: vault` (namespace `vault`) | Flux waits for Vault before installing |
| `address: http://vault.vault.svc.cluster.local:8200` | the in-cluster Vault from [`../vault/`](../vault/README.md) |
| `skipTLSVerify: false` | TLS verification on — though the address is plain HTTP, so it does not apply |
| `--client-cache-persistence-model=direct-encrypted` | the client cache is persisted, encrypted, so the operator does not re-authenticate from scratch on restart |

The values block has an indentation problem worth checking: `defaultVaultConnection:` is declared and
then `enabled`, `address`, `skipTLSVerify` and `spec` sit at the same level as it rather than nested
under it. As written, those are top-level chart values rather than fields of the default connection.
This is the kind of thing that silently produces a working install with no default connection.

**No `VaultAuth`, `VaultStaticSecret` or `VaultDynamicSecret` exists anywhere in this repository**, so
the operator is installed with nothing to reconcile.

### The overlap to resolve

This is the thing to take away from the folder. Three consumption paths against the same Vault are
present in this repository:

| Path | State |
|---|---|
| [external-secrets](../../../integrations/external-secrets/README.md) | **configured and working** — a `ClusterSecretStore` against `http://vault.vault:8200`, path `pikakube` |
| Vault Secrets Operator (here) | installed, no CRs |
| [Bank-Vaults](../vault-operator/README.md) | installed, and a different kind of tool — it *runs* Vault rather than consuming from it |

Exactly one consumption path should be live. The honest case for each: external-secrets is already
working and covers Azure Key Vault too, which is also in use here; VSO would be the better choice if
this platform adopted **dynamic** database credentials, because lease handling and
`rolloutRestartTargets` are precisely what that requires and precisely what external-secrets does not
do well.

Since nothing here uses dynamic secrets yet — every recorded example is static KV — external-secrets
is the defensible choice today, and this folder is the one to revisit when Airflow's PostgreSQL
credentials become dynamic.

---

[← Vault](../README.md)
