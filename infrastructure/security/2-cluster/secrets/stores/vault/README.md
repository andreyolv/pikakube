[← Secret stores](../README.md)

# Vault

HashiCorp Vault, plus the two competing operators and a dev-mode deployment that live beside it.

Subfolders: [`vault/`](vault/README.md) — the real deployment ·
[`vault-dev/`](vault-dev/README.md) — in-memory, for tutorials ·
[`vault-secrets-operator/`](vault-secrets-operator/README.md) — HashiCorp's operator ·
[`vault-operator/`](vault-operator/README.md) — Bank-Vaults' operator

## Contents

1. [What is in this folder](#1-what-is-in-this-folder)
2. [The four ways to get a Vault secret into a pod](#2-the-four-ways-to-get-a-vault-secret-into-a-pod)
3. [Deployment shapes: dev, standalone, HA](#3-deployment-shapes-dev-standalone-ha)
4. [The two operators are not the same kind of thing](#4-the-two-operators-are-not-the-same-kind-of-thing)
5. [Anti-patterns](#5-anti-patterns)
6. [How this applies to pikakube](#6-how-this-applies-to-pikakube)

---

## 1. What is in this folder

Four subfolders, and they answer three different questions. Read the layout before assuming they
are alternatives:

| Folder | What it is |
|---|---|
| [`vault/`](vault/README.md) | a Vault server with persistent storage, audit storage, UI, ingress, metrics, and an auto-unseal script |
| [`vault-dev/`](vault-dev/README.md) | the same chart in dev mode — in-memory, always unsealed, root token `root` |
| [`vault-secrets-operator/`](vault-secrets-operator/README.md) | HashiCorp's own operator, syncing Vault → Kubernetes `Secret` |
| [`vault-operator/`](vault-operator/README.md) | Bank-Vaults' operator, which *runs and configures* Vault rather than consuming from it |

Both `vault/` and `vault-dev/` deploy a `HelmRelease` named `vault` into the namespace `vault`.
They are two versions of the same thing, not two components, and only one can be applied at a time.

## 2. The four ways to get a Vault secret into a pod

This is the decision that generates the most confusion, because HashiCorp ships three answers and
the community ships a fourth. HashiCorp's own comparison of the first three is at
<https://www.hashicorp.com/blog/kubernetes-vault-integration-via-sidecar-agent-injector-vs-csi-provider>.

| Method | Shape | Result | Notes |
|---|---|---|---|
| **Agent Sidecar Injector** | a mutating webhook injects a Vault Agent sidecar and init container | files under `/vault/secrets`, rendered from templates | the oldest approach; a sidecar per pod, and templating in annotations |
| **Vault CSI Provider** | a plugin for [secrets-store-csi-driver](../../integrations/secrets-store-csi-driver/README.md) | files in a CSI volume | no Kubernetes `Secret` unless `syncSecret` is on |
| **Vault Secrets Operator** | a controller with CRDs | a Kubernetes `Secret` | HashiCorp's current recommendation; see [`vault-secrets-operator/`](vault-secrets-operator/README.md) |
| **external-secrets** | a vendor-neutral controller with CRDs | a Kubernetes `Secret` | not HashiCorp's; supports many stores behind one API — [`../../integrations/external-secrets/`](../../integrations/external-secrets/README.md) |

Both `injector` and `csi` are explicitly disabled in the Helm values in this repo
(`injector.enabled: false`, `csi.enabled: false`), which narrows the choice here to the two
operator-shaped options.

Choosing between the last two: Vault Secrets Operator is deeper — it understands Vault's dynamic
secrets, leases and rotation as first-class concepts, and can trigger rollouts on rotation.
external-secrets is broader — one API across Vault, Azure Key Vault, AWS Secrets Manager and
others, which matters if Vault might not be the only store forever. Running both against the same
Vault is a way to have two sources of truth for the same `Secret`.

## 3. Deployment shapes: dev, standalone, HA

| Mode | Storage | Sealed? | Survives a restart? | For |
|---|---|---|---|---|
| **Dev** | in-memory | never — permanently unsealed | no, everything is lost | tutorials only |
| **Standalone** | one PVC, file or Raft backend | yes, needs unsealing | yes | a single-node learning or non-critical cluster |
| **HA** | Raft across 3 or 5 replicas | yes, each node needs unsealing | yes | anything real |

Dev mode is the one to be careful about, because it looks like it works. `server.dev.enabled: true`
gives a Vault with a UI, an API, and a root token of literally `root` — recorded in the
`vault-dev/` notes as visible in the pod log. It is genuinely useful for learning the CLI and for
testing an integration. It is not a Vault, and any secret put into it disappears at the next pod
restart.

Standalone with persistence is what `vault/` in this repo is: a data PVC, an audit PVC, and an init
script. Going from there to HA is a values change plus the operational commitments in
[`../README.md`](../README.md#6-operating-cost-stated-plainly).

## 4. The two operators are not the same kind of thing

This is the trap in this folder. They have similar names and opposite jobs:

| | vault-secrets-operator (HashiCorp) | vault-operator (Bank-Vaults) |
|---|---|---|
| Direction | reads *from* Vault into the cluster | *creates and configures* Vault itself |
| CRDs | `VaultStaticSecret`, `VaultDynamicSecret`, `VaultPKISecret`, `VaultConnection`, `VaultAuth` | `Vault` — a declarative Vault instance |
| Replaces | external-secrets, the injector, the CSI provider | the Helm chart plus the manual `vault operator init` / `unseal` / `policy write` steps |
| Assumes | a Vault already exists | it will run Vault for you |
| Needs the other? | yes, it needs a Vault | no, but you still need a way to consume secrets |

Bank-Vaults' proposition is that everything a Vault operator does by hand — the init, the unseal,
the auth backends, the policies — becomes fields in a `Vault` custom resource, which is a real
answer to the configuration-drift problem this folder otherwise leaves open. Its companion
`secrets-webhook` handles injection into pods, so the Bank-Vaults stack is an alternative to the
HashiCorp stack rather than a component of it.

Having both plus external-secrets in one repository is an evaluation, not a design. Exactly one
consumption path should end up live.

## 5. Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Applying `vault/` and `vault-dev/` together | both are a `HelmRelease` named `vault` in namespace `vault` | pick one per cluster |
| Dev mode anywhere that holds a real secret | in-memory, root token `root`, gone on restart | standalone with persistence at minimum |
| The unseal key in the HelmRelease | the key is in Git next to the encrypted data | KMS auto-unseal, or manual unseal with shares held elsewhere |
| Two consumption paths against one Vault | two controllers writing the same `Secret`, fighting | one of VSO, external-secrets, injector, or CSI |
| Confusing the two operators | one reads from Vault, the other runs Vault | read [section 4](#4-the-two-operators-are-not-the-same-kind-of-thing) before installing either |
| The root token kept in use after setup | it bypasses every policy | revoke it and use policy-bound tokens or Kubernetes auth |
| Configuring Vault by hand and not writing it down | the cluster is unreproducible; `init.sh` becomes tribal knowledge | Bank-Vaults' `Vault` CR, or Terraform's Vault provider |
| Single replica with `dependsOn` from every consumer | a Vault restart stalls everything downstream | HA, plus a consumption path that degrades gracefully |

## 6. How this applies to pikakube

The `vault/` deployment is the interesting one and is shaped like something real: persistent data
and audit storage, the UI exposed through ingress with a mkcert TLS secret and a Forecastle
annotation, and `serverTelemetry.serviceMonitor` on so Prometheus scrapes it. The injector and CSI
provider are both off, which is a clear decision.

Its one local-only compromise is auto-unseal: `VAULT_AUTO_UNSEAL_KEY_0: pikakube` in the values,
consumed by a `postStart` script from a ConfigMap. That makes a local cluster restart painless and
makes the seal decorative. It is the right call for this repo and the first thing to change if this
shape is ever copied.

Consumption is currently done by **external-secrets**, which has a working `ClusterSecretStore`
pointing at `http://vault.vault:8200` with `path: pikakube`. Vault Secrets Operator is deployed
alongside it with `dependsOn: vault` and a default connection to the same address, which means two
controllers are installed for the same job. Bank-Vaults' operator is a third path and is deployed
from an `OCIRepository` in `flux-system` with empty values.

The recorded `init.sh` is the honest picture of what running this costs today: port-forward,
`vault operator init`, save the keys, unseal three times, log in, enable a KV engine, write a
policy, create a token. Every one of those steps is manual and none of it is in Git. That gap is
precisely what Bank-Vaults' `Vault` CR exists to close, and it is the strongest argument for the
folder that currently has the least configuration in it.

---

[← Secret stores](../README.md)
