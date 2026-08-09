[← Secrets](../README.md)

# Secret stores

A dedicated system owns the secret. Nothing sensitive is in Git, rotation happens in one place, and
you now operate a stateful service that everything depends on.

Tools: [`vault/`](vault/README.md) — the reference, plus its operators ·
[`openbao/`](openbao/README.md) — the open-source fork of Vault ·
[`infisical/`](infisical/README.md) — developer-facing, lighter to run

## Contents

1. [What a store gives you that encryption does not](#1-what-a-store-gives-you-that-encryption-does-not)
2. [Dynamic secrets](#2-dynamic-secrets)
   - [Why it changes the threat model](#why-it-changes-the-threat-model)
   - [What it requires from the application](#what-it-requires-from-the-application)
3. [Authentication: how a pod proves who it is](#3-authentication-how-a-pod-proves-who-it-is)
4. [The seal, and the bootstrap problem](#4-the-seal-and-the-bootstrap-problem)
5. [The licence change and OpenBao](#5-the-licence-change-and-openbao)
6. [Operating cost, stated plainly](#6-operating-cost-stated-plainly)
7. [Anti-patterns](#7-anti-patterns)
8. [How this applies to pikakube](#8-how-this-applies-to-pikakube)

---

## 1. What a store gives you that encryption does not

[`../encryption/`](../encryption/README.md) solves "how do I keep a secret in Git safely". A store
solves a different and larger set of problems:

| Capability | encryption/ | stores/ |
|---|---|---|
| Secret never touches Git | no — it is in Git, encrypted | yes |
| Rotate a value in one place | commit and reconcile everywhere | change it; consumers pick it up |
| Audit log of **reads** | impossible | yes, per request, per identity |
| Revoke access to a specific consumer | not a concept | yes, by policy |
| Generate credentials on demand | no | yes — see [section 2](#2-dynamic-secrets) |
| Encryption as a service (transit) | no | yes — encrypt application data without the app holding a key |
| Certificate issuance | no | yes — a PKI engine |
| Works with the cluster down | not applicable | yes, it is external |
| Extra system to operate | none | a stateful, HA, always-on dependency |

The read audit is the underrated one. With encrypted files there is no answer to "who read this
credential and when"; with a store, every access is attributable, which is what makes an incident
investigable.

## 2. Dynamic secrets

The capability that actually justifies the operational cost, and the one people skip past on their
way to using Vault as an encrypted key-value store.

A **static** secret exists before anyone needs it, is shared by everything that uses it, and stays
valid until someone remembers to change it. A **dynamic** secret is created at the moment of the
request:

```
app → store: "I need database access"
store → database: CREATE ROLE v-app-a1b2c3 ... VALID UNTIL now() + 1h
store → app: username v-app-a1b2c3, password ...
[one hour later]
store → database: DROP ROLE v-app-a1b2c3
```

The store holds a privileged credential for the backend, and hands out short-lived derived ones.
This works for databases (PostgreSQL, MySQL, MongoDB), cloud IAM (AWS, Azure, GCP), SSH, RabbitMQ,
and PKI.

### Why it changes the threat model

| Static | Dynamic |
|---|---|
| Valid until rotated — often years | valid for the lease TTL — often an hour |
| Identical across every replica and often every environment | unique per lease |
| A leaked credential is a live credential | a leaked credential is usually already expired |
| "Who used this?" — unanswerable, it is the same string everywhere | each lease maps to one requester |
| Rotation is a coordinated change across all consumers | rotation is the normal operation |
| Revocation means changing it everywhere at once | revoke one lease |

This is not achievable by encrypting a static password more carefully. It is the one thing on this
page that a Git-based approach structurally cannot do.

### What it requires from the application

Nothing is free:

- The application must **re-read** the credential when the lease renews, or be restarted. An app
  that opens a connection pool at startup with a one-hour credential will fail at minute 61 in a
  way that looks like a database problem.
- The store needs a privileged credential on the backend — a Vault compromise is now a database
  compromise. That privileged credential should itself be rotatable, and Vault can rotate its own.
- Connection churn goes up, and every dynamic credential is a real role in the database. Leases that
  are not revoked accumulate as roles.

The honest advice: adopt dynamic secrets where the consumer already handles credential refresh
(most operators, most modern SDKs) and keep static secrets for the things that do not, rather than
adopting it everywhere and discovering the failure at 3am.

## 3. Authentication: how a pod proves who it is

A store is only as good as its answer to "who is asking". This is the chicken-and-egg problem of
the whole folder: if a pod needs a credential to fetch credentials, nothing has been solved.

| Method | How it works | Verdict |
|---|---|---|
| **Kubernetes auth** | the pod presents its ServiceAccount token; the store verifies it against the API server's `TokenReview` and maps ServiceAccount + namespace to a policy | the right answer inside a cluster — no stored credential at all |
| **JWT/OIDC auth** | the store validates a signed token against an issuer | the right answer for CI and cross-cluster |
| **AppRole** | a role ID plus a secret ID | a stored credential again; workable but you are back to distributing something |
| **Token** | a long-lived token in a Kubernetes Secret | the bootstrap credential you were trying to avoid |

The Kubernetes auth method is the one to use, and it is what the tutorial in
`../integrations/secrets-store-csi-driver/example/` demonstrates: enable it, point it at the API
server, then bind a role to a specific ServiceAccount in a specific namespace with a specific
policy and TTL.

The `ClusterSecretStore` in `../integrations/external-secrets/hashicorp-vault/` uses the *token*
method instead — `tokenSecretRef` pointing at a Kubernetes Secret containing a Vault token. That is
the quickest way to get something working and the thing to replace first: the token is a static
credential in a Secret, which is exactly what the store was supposed to eliminate.

## 4. The seal, and the bootstrap problem

Vault and OpenBao encrypt their storage with a master key that they do not hold at rest. On start
they are **sealed**: running, reachable, and refusing to do anything until the key is reassembled
from unseal shares.

This is a genuine security property — an attacker with the storage volume has ciphertext — and a
genuine operational problem: **a restarted Vault serves nothing until it is unsealed.** If secrets
delivery is on the critical path of your deployments, a node reboot at the wrong moment stops
deployments cluster-wide.

Three answers:

| Approach | Trade-off |
|---|---|
| Manual unseal (`vault operator unseal`, three times with three shares) | the strongest, and it means a human must be present after every restart |
| Auto-unseal via cloud KMS | the KMS holds the key; unattended restarts work; you have moved the trust to the cloud provider, which is usually correct |
| Auto-unseal with a key in configuration | unattended, and the seal now protects nothing, because the key is next to the lock |

The third one is what `vault/vault/helm/helmrelease.yaml` does in this repo:
`VAULT_AUTO_UNSEAL_KEY_0: pikakube`, consumed by an init script in a ConfigMap. That is a
deliberate convenience for a local learning cluster and must not travel anywhere else — the unseal
key is in Git.

Related: dev mode (`server.dev.enabled: true`) is a different thing again — in-memory storage,
permanently unsealed, root token literally `root`. Everything is lost on restart. It is for
tutorials, and both `vault/vault-dev/` and `openbao/` in this repo run in it.

## 5. The licence change and OpenBao

In August 2023 HashiCorp relicensed its products, Vault included, from MPL 2.0 to the **Business
Source License**. BSL is not open source: it forbids use that competes with the licensor, and each
version converts to MPL after four years.

The practical impact for most users is nil — running Vault to hold your own secrets is not
competing with HashiCorp. The impact for anyone embedding, reselling, or offering it as a managed
service is real, and the impact on Linux distributions and downstream packaging was immediate.

**OpenBao** is the fork of the last MPL-licensed Vault, donated to the Linux Foundation. It is
API-compatible, so clients, the Helm chart shape, and integrations transfer with little change. It
has since diverged with its own features.

Choosing between them:

| Pick Vault if | Pick OpenBao if |
|---|---|
| You want HashiCorp support or Vault Enterprise features (HSM, namespaces, replication) | the licence matters to you legally or on principle |
| You need an ecosystem integration that only targets Vault | you want a Linux Foundation-governed project |
| The team already knows it | you are starting fresh and want no licence question |

Both are in this repo, which is the sensible way to keep the option open.

## 6. Operating cost, stated plainly

A store is a distributed, stateful, HA system on the critical path of deployments. Before adopting
one, the checklist is:

- **Storage backend.** Raft (integrated) is the modern default and means an odd-numbered cluster
  with consensus. It is a database you now own.
- **Backup and restore.** Of the storage *and* the unseal material. Tested.
- **Unseal strategy.** See [section 4](#4-the-seal-and-the-bootstrap-problem). Decide before the
  first restart, not after.
- **Availability.** If Vault is down, can pods start? With external-secrets, already-synced Secrets
  survive; with the CSI driver, a new pod cannot mount.
- **Audit device.** Off by default in some configurations, and the audit log is half the reason to
  run a store. Note that Vault will *block* if it cannot write to an enabled audit device — that is
  intentional and it has caused outages.
- **Policy sprawl.** Every consumer needs a policy. Without a convention, this becomes hundreds of
  hand-written HCL files.

If the answer to "do we need dynamic secrets, read auditing, or revocation" is no, then
[`../encryption/`](../encryption/README.md) does the job with none of the above.

## 7. Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Running a store as an encrypted key-value store only | you took on an HA stateful dependency and used the one feature SOPS already gives you | use dynamic secrets, or use encryption instead |
| Dev mode as a real deployment | in-memory, root token `root`, everything lost on restart | dev mode for tutorials only |
| Auto-unseal key committed in configuration | the seal protects nothing | KMS auto-unseal, or manual unseal with shares held separately |
| Token auth for the Kubernetes integration | a static long-lived credential in a Secret — the problem you were solving | Kubernetes auth via ServiceAccount `TokenReview` |
| One policy granting broad paths | any consumer compromise reads everything | one policy per consumer, scoped to its path |
| No audit device | no answer to "who read this and when", which was half the point | enable one, and monitor that it can write |
| Single replica | every restart is a full outage of secrets delivery | HA with Raft, and a PDB |
| No tested restore | the backup is a hypothesis | restore into a scratch cluster and verify |
| Dynamic secrets for an app that reads config once | it fails at lease expiry, and the failure looks like a database problem | pair with a restart mechanism, or keep it static |
| Long-lived root token in circulation | it bypasses every policy | generate one for setup, revoke it, use policies afterwards |

## 8. How this applies to pikakube

Three stores are here and all three are in a local-cluster shape.

[`vault/`](vault/README.md) is the most built out and contains four things, not one: a
production-shaped Vault (Raft storage, audit storage enabled, UI, ingress, `ServiceMonitor`), a
dev-mode Vault, HashiCorp's [Vault Secrets Operator](vault/vault-secrets-operator/README.md), and
Bank-Vaults' [vault-operator](vault/vault-operator/README.md). Two of those are competing ways to
get secrets into the cluster, and a third exists in
[`../integrations/`](../integrations/README.md) — external-secrets, which is the one actually
configured against this Vault.

[`openbao/`](openbao/README.md) runs with `server.dev.enabled: true`, so it is there to be looked
at rather than used, but it is the version that resolves the licence question if that ever matters.

[`infisical/`](infisical/README.md) is deployed as its Kubernetes **operator** only — the operator
syncs secrets from an Infisical instance, which is not part of this repo, so it is the least
complete of the three.

Nothing here is currently using dynamic secrets: the recorded tutorials all put static key-value
pairs into a KV engine (`vault kv put andreyolv/senha ...`,
`vault kv put airflow/connections/smtp_default ...`). That is the right way to learn the tool, and
it is also the configuration where a store is hardest to justify over SOPS. The change that would
make Vault genuinely worth its cost on this platform is a database secrets engine issuing
short-lived PostgreSQL credentials to Airflow — the credentials are already in Vault
(`airflow/connections/`), just as static values.

---

[← Secrets](../README.md)
