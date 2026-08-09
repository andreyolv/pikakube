[← Vault](../README.md)

# HashiCorp Vault

<https://github.com/hashicorp/vault>
<https://github.com/hashicorp/vault-helm>
<https://github.com/hashicorp/vault-csi-provider>
<https://github.com/hashicorp/vault-secrets-operator>

The reference secrets management system. Persistent deployment with audit storage, UI and ingress.

---

## The problem it solves

Everything in [`../../../encryption/`](../../../encryption/README.md) moves a static credential around more
safely. Vault does four things that no Git-based approach can:

| Capability | What it means |
|---|---|
| **Dynamic secrets** | credentials generated per request with a TTL, then revoked automatically — the genuinely different capability, see [`../../README.md`](../../README.md#2-dynamic-secrets) |
| **Read audit** | every access attributable to an identity, which is what makes an incident investigable |
| **Revocation** | remove a policy and access stops, without re-encrypting anything |
| **Encryption as a service** | the `transit` engine encrypts application data without the application ever holding a key |

Plus a PKI engine that issues short-lived certificates, and a long list of auth methods so consumers
can prove identity without a stored credential.

The architecture in one paragraph: storage is encrypted with a master key that Vault does not hold at
rest, so it starts **sealed** and refuses everything until unsealed. Secrets are organised into
mounted **engines** (`kv`, `database`, `pki`, `transit`, ...), access is granted by **policies**
written in HCL against paths, and identity is established by an **auth method** — Kubernetes,
JWT/OIDC, AppRole, or a token.

The pieces that matter most on Kubernetes:

- **Kubernetes auth.** A pod presents its ServiceAccount token; Vault verifies it with the API
  server's `TokenReview` and maps ServiceAccount + namespace to a policy. No stored credential at
  all. This is the correct answer, and it is demonstrated in
  [`../../../integrations/secrets-store-csi-driver/`](../../../integrations/secrets-store-csi-driver/README.md).
- **Four ways to reach a pod** — agent injector, CSI provider, Vault Secrets Operator, or
  external-secrets. Compared in [`../README.md`](../README.md#2-the-four-ways-to-get-a-vault-secret-into-a-pod).

## When to use it

- **Dynamic database credentials.** The clearest justification: Vault holds one privileged
  PostgreSQL credential and issues short-lived per-consumer roles. A leaked credential expires by
  itself.
- **Read auditing is required.** "Who read this credential and when" has no answer with encrypted
  files.
- **Many consumers, many environments.** Rotation in one place beats a commit that touches every
  environment.
- **Short-lived cloud credentials.** The AWS/Azure/GCP engines issue temporary IAM credentials
  instead of storing static keys — though workload identity is better still where it exists.
- **Internal PKI.** Short-lived certificates issued on demand, with cert-manager able to use Vault as
  an issuer.
- **Encryption as a service.** Applications that must encrypt data without holding a key.

## When not to use it

- **As an encrypted key-value store and nothing else.** If the only engine in use is `kv` with static
  values, you have taken on an HA stateful dependency to get what
  [SOPS](../../../encryption/sops/README.md) provides with a file and a key. This is the most common
  way Vault fails to pay for itself, and it is the current state of this deployment — see the Notes.
- **For bootstrap credentials.** Something must authenticate to Vault, and Vault must be running.
  Bootstrap belongs in [`../../../encryption/`](../../../encryption/README.md).
- **Without an unseal plan.** A restarted Vault serves nothing until unsealed. If secret delivery is
  on the deployment critical path, a node reboot at the wrong moment stops deployments cluster-wide.
- **Single replica.** Every restart is a full outage of secrets delivery.
- **Without an audit device and a tested restore.** The audit log is half the reason to run it, and
  a backup that has never been restored is a hypothesis.
- **If the licence matters.** Vault moved to the Business Source License in 2023.
  [OpenBao](../../openbao/README.md) is the open fork — see
  [`../../README.md`](../../README.md#5-the-licence-change-and-openbao).

## Notes

Every original note from `doc.md`, plus `init.sh` and `mypolicy.hcl`, translated and explained.

### Comparing the three HashiCorp integrations

> Comparison of the 3 approaches
> <https://www.hashicorp.com/blog/kubernetes-vault-integration-via-sidecar-agent-injector-vs-csi-provider>

HashiCorp's own comparison of the agent injector, the CSI provider, and (in later revisions) the
Vault Secrets Operator. The short version, expanded in [`../README.md`](../README.md#2-the-four-ways-to-get-a-vault-secret-into-a-pod):
the injector adds a sidecar per pod and renders templates to files; the CSI provider mounts a volume
and creates no `Secret`; the operator produces a `Secret` and understands leases and rotation.

Both `injector.enabled` and `csi.enabled` are set to `false` in this deployment, so the choice here
has already been narrowed to the operator-shaped options.

### CSI provider

> <https://developer.hashicorp.com/vault/tutorials/kubernetes/kubernetes-secret-store-driver>

The Vault provider for the Kubernetes SIG
[secrets-store-csi-driver](../../../integrations/secrets-store-csi-driver/README.md). The worked
example in that folder — Kubernetes auth, a scoped policy, a role bound to one ServiceAccount in one
namespace — is the best authentication reference in this repository.

### Sidecar injector

> <https://developer.hashicorp.com/vault/tutorials/kubernetes/kubernetes-sidecar>
> <https://github.com/hashicorp-education/learn-vault-kubernetes-sidecar>

The oldest integration: a mutating webhook injects an init container and a sidecar running Vault
Agent, which authenticates, fetches secrets, renders them through a template into `/vault/secrets`,
and keeps them refreshed. Configured entirely through pod annotations.

Its advantage is that no Kubernetes `Secret` is created and the agent handles token renewal and
lease refresh. Its cost is a sidecar in every pod and templating expressed in annotations, which
becomes unreadable quickly. Disabled here.

### Installing the CLI

> <https://developer.hashicorp.com/vault/install#linux>

The `vault` binary is needed for every command in `init.sh`. It talks to the HTTP API, so it works
against a port-forward from anywhere.

### Initialising Vault, step by step

The file is a written procedure, not an executable script. Translated and annotated:

```bash
k port-forward service/vault 8200
export VAULT_ADDR="http://127.0.0.1:8200"
```

Reach Vault locally. The CLI takes its address from `VAULT_ADDR`.

```bash
vault operator init
# save the keys and token
```

The one-time initialisation. It prints **five unseal key shares** and an **initial root token**, and
prints them exactly once — losing them means losing the data permanently. Three of the five shares
are required to unseal (Shamir's Secret Sharing), which is the design: no single person can unseal
Vault alone.

```bash
vault status
vault operator unseal   # ×3
vault login             # paste the root token
```

`unseal` is run three times, once per share, by three different holders in a real setup. Until then
Vault is running and refusing everything.

```bash
vault secrets enable -path=andreyolv kv
vault kv put andreyolv/senha palavra1=giropops palavra2=strigus
vault kv get andreyolv/senha
```

Mount a KV engine at the path `andreyolv` and write a secret with two keys. Note this enables **KV
v1** — `-version=2` would be needed for the versioned engine, and the version changes the API path
(`/data/` is inserted), which is a common source of confusing 404s. The
[external-secrets ClusterSecretStore](../../../integrations/external-secrets/README.md) in this repo
declares `version: v2` against a `pikakube` path, so it is a different mount from this one.

```bash
vault policy write mypolicy mypolicy.hcl
vault token create -policy="mypolicy"
# save the token
```

`mypolicy.hcl` beside the script is three lines and is the whole authorisation model in miniature:

```hcl
path "andreyolv/senha" {
    capabilities = ["read"]
}
```

Read, one path, nothing else. Everything not granted is denied — Vault policies are deny-by-default,
which is why a policy is short.

The token created from it is a static, long-lived credential, and it is the pattern to move away
from: [Kubernetes auth](../../README.md#3-authentication-how-a-pod-proves-who-it-is) binds a policy
to a ServiceAccount instead, with nothing stored.

```
To log into the UI, access the vault-0 pod and run the commands to create a user:
k port-forward svc/vault-ui 8210:8200
Method Token, and pass the Initial Root Token
```

Reaching the UI over a second port-forward, authenticating with the token method. Using the **root
token** for this is fine during setup and wrong afterwards — the root token bypasses every policy and
should be revoked once real auth methods exist.

The honest summary of this file: **every step is manual and none of it is in Git.** The cluster's
Vault configuration cannot be rebuilt from this repository. That gap is exactly what
[Bank-Vaults' vault-operator](../vault-operator/README.md) exists to close, and it is the strongest
argument in this subtree for the folder with the least configuration in it.

### How it is deployed here

`helm/helmrelease.yaml`, chart `vault` 0.30.0:

| Setting | Meaning |
|---|---|
| `server.dataStorage: 2Gi`, `auditStorage.enabled: true` (2Gi) | persistent storage, and an audit device volume — the audit log is half the point of a store |
| `server.ingress` | UI exposed at `vault.127.0.0.1.nip.io` with `mkcert-tls-secret` and Forecastle annotations |
| `ui.enabled: true` | the web UI |
| `injector.enabled: false`, `csi.enabled: false` | two of the four integrations deliberately off |
| `serverTelemetry.serviceMonitor.enabled: true` | Prometheus scrapes it |
| `server.postStart` → `/vault/userconfig/init/init.sh` | runs a script from the `vault-init` ConfigMap after the container starts |
| `extraEnvironmentVars.VAULT_AUTO_UNSEAL_KEY_0: pikakube` | **the unseal key, in the HelmRelease, in Git** |

That last row is the one to be explicit about. `configmap.yaml` holds a `vault-init.sh` that runs
`vault operator unseal $VAULT_AUTO_UNSEAL_KEY_0`, so the pod unseals itself on every restart with a
key committed to the repository. For a local learning cluster that is a sensible convenience —
without it, every `kind` restart requires manual unsealing. Anywhere else, it means the seal protects
nothing, and the replacement is KMS auto-unseal.

Note also the `postStart` in the HelmRelease points at `init.sh` while the ConfigMap provides
`vault-init.sh` — worth checking, since the two names do not match and a `postStart` failure is easy
to miss.

Consumption is currently through
[external-secrets](../../../integrations/external-secrets/README.md), authenticating with a static
token. And nothing here uses a dynamic secrets engine: everything is static KV, which is the
configuration in which Vault is hardest to justify over SOPS. The change that would make it worth
the cost is a `database` engine issuing short-lived PostgreSQL credentials — the Airflow connections
recorded in [`../vault-dev/`](../vault-dev/README.md) are already in Vault, just as static values.

---

[← Vault](../README.md)
