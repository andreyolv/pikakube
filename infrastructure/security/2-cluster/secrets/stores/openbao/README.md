[← Secret stores](../README.md)

# OpenBao

<https://github.com/openbao/openbao>
<https://github.com/openbao/openbao-helm>

The open-source fork of HashiCorp Vault, created after Vault moved to the Business Source License.
Linux Foundation governed, API-compatible.

---

## The problem it solves

In August 2023 HashiCorp relicensed its products — Vault, Terraform, Consul, Nomad — from MPL 2.0 to
the **Business Source License**. BSL is not an open source licence: it forbids use that competes with
the licensor, and each version converts to MPL four years after release.

For most users the practical impact is zero. Running Vault to hold your own secrets is not competing
with HashiCorp. The impact is real for anyone who:

- embeds it in a product,
- offers it as a managed service,
- packages it for a Linux distribution,
- or works somewhere with a policy requiring OSI-approved licences.

That last category is larger than it sounds, and it is the reason the fork exists at all.

**OpenBao** is a fork of the last MPL-licensed Vault, donated to the Linux Foundation. It is
API-compatible, so:

| Transfers directly | Notes |
|---|---|
| The HTTP API | clients and SDKs work unchanged |
| The CLI | `bao` is the command; `vault` semantics are preserved |
| Secrets engines | KV, database, PKI, transit |
| Auth methods | Kubernetes, JWT/OIDC, AppRole |
| Policies | the same HCL |
| The Helm chart shape | recognisably the same values structure |

It has since diverged, adding features of its own and removing HashiCorp's enterprise hooks. The
divergence grows over time, so "API-compatible" is a statement about today rather than a permanent
guarantee.

Everything in [`../README.md`](../README.md) about dynamic secrets, the seal, and authentication
applies here unchanged — this is Vault's architecture.

## When to use it

- **The licence matters legally or on principle.** The whole reason it exists. If a policy requires
  OSI-approved licences, this is the version that qualifies.
- **You are starting fresh.** There is no migration cost, and no licence question to revisit later.
- **Foundation governance matters to you.** Linux Foundation stewardship rather than a single
  vendor, which is a real consideration for infrastructure you expect to run for years.
- **You want Vault's model without the vendor relationship.** Dynamic secrets, PKI, transit
  encryption, Kubernetes auth — all of it.
- **Migrating away from Vault.** API compatibility makes it the least disruptive destination.

## When not to use it

- **You need Vault Enterprise features.** HSM support, namespaces, performance replication, disaster
  recovery replication. Those are HashiCorp's commercial product and have no equivalent here.
- **You want vendor support.** HashiCorp sells it; OpenBao has community support and whatever a
  third party offers.
- **An integration only targets Vault.** Most speak the API and work with both, and some do not.
  [Vault Secrets Operator](../vault/vault-secrets-operator/README.md) is HashiCorp's and targets
  Vault; [external-secrets](../../integrations/external-secrets/README.md) is vendor-neutral and is
  the safer choice alongside OpenBao. Check before assuming.
- **The team already runs Vault well.** Migrating a working secrets store to resolve a licence
  question that does not affect you is work with no return.
- **You need long-term ecosystem certainty.** It is younger, with a smaller community, and the
  divergence from Vault will grow. That is a normal fork risk and it should be stated rather than
  glossed over.

## Notes

The original `doc.md` contained only the two repository links, which are at the top of this file.
What follows is the state of this deployment.

### How it is deployed here

`helm/ocirepository.yaml` — an `OCIRepository` in the `openbao` namespace pointing at
`oci://ghcr.io/openbao/charts/openbao`, pinned to **both** a tag (`0.28.6`) and a digest
(`sha256:b3a8d9...`).

That double pin is the right pattern and is worth calling out: a tag can be moved, a digest cannot,
so the chart that gets installed is byte-identical on every reconcile. The same pattern is used by
[Kyverno](../../../policies/kyverno/README.md) in this repo, and notably **not** by
[vault-operator](../vault/vault-operator/README.md), whose `ref` block is commented out entirely.

`helm/helmrelease.yaml` uses `chartRef` against that `OCIRepository` — the modern Flux form — with:

| Setting | Meaning |
|---|---|
| `server.dev.enabled: true` | **dev mode**: in-memory, permanently unsealed, root token `root`, everything lost on restart |
| `server.ingress` | UI at `openbao.127.0.0.1.nip.io`, `mkcert-tls-secret`, Forecastle annotations grouping it under "Security" |

Dev mode is the thing to be clear about. This deployment is here to be looked at and clicked through,
not used: no storage, no seal, no persistence. Everything in
[`../vault/vault-dev/`](../vault/vault-dev/README.md) about the trap of dev mode applies equally —
it looks like a working store right up until the pod restarts.

The commented-out Forecastle icon annotation still points at the **HashiCorp Vault** logo, which is a
small but honest reflection of where the fork sits: same shape, same tooling, different project.

### Vault or OpenBao, for this platform

Both are deployed here, which is the sensible way to keep the option open while the question is not
yet forced.

Two things would decide it:

1. **Does the licence matter?** For a personal or internal learning platform, no. For anything
   commercial or distributed, it is the deciding question and OpenBao answers it.
2. **Which consumption path?** [`../vault/`](../vault/README.md) has the more developed
   configuration, but the operator installed alongside it —
   [Vault Secrets Operator](../vault/vault-secrets-operator/README.md) — is HashiCorp's and pairs
   with Vault. The path that works with either is
   [external-secrets](../../integrations/external-secrets/README.md), which is also the one already
   configured in this repository. That makes external-secrets the choice that leaves the store
   question open.

If OpenBao were to become the real store here, the changes needed are the same ones listed for Vault:
turn off dev mode, add persistent storage, decide on an unseal strategy that does not put the key in
Git, enable an audit device, and use the Kubernetes auth method instead of a static token.

---

[← Secret stores](../README.md)
