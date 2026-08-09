[← Admission control](../README.md)

# Connaisseur

<https://github.com/sse-secure-systems/connaisseur>

Deployment: [`helm/`](helm/README.md)

---

## The problem it solves

Connaisseur is an admission controller for image signature verification, and its distinguishing
feature is that **signature format is pluggable**. Where the Sigstore controller verifies
Sigstore, Connaisseur has a validator abstraction:

| Validator | Verifies |
|---|---|
| **Cosign / Sigstore** | key-based and keyless signatures, with Rekor and Fulcio |
| **Notary v1** | Docker Content Trust — the older format, still present in some registries and enterprise estates |
| **Notation / Notary v2** | the newer OCI-native signing specification |
| `static` | unconditional allow or deny, for images that will never be signed |

That matters in exactly one situation, and it is a real one: **an estate with more than one
signing format**. A migration from Docker Content Trust to Cosign takes months, and during it
both must be verifiable by the same controller.

The other reason it gets chosen is that its configuration is built around the rollout, not around
the ideal end state. Image policies are expressed as a list of glob patterns mapped to
validators, with a default rule at the bottom, and **detection mode** turns the whole thing into
logging rather than rejection. That structure makes "verify these images, allow the rest, tell me
what would have failed" the natural first configuration rather than something you assemble.

It also resolves tags to digests and pins them, closing the race described in
[`../README.md`](../README.md) section 2.

## When to use it

- **More than one signature format in play** — Notary v1 alongside Cosign is the case it wins
- **A migration between signing schemes**, where both must be accepted for a period
- **You want the gentlest rollout.** Detection mode plus glob-based policy makes incremental
  adoption straightforward
- **Per-image-pattern policy is the natural shape** of your requirement — "images from our
  registry must be signed by us, images from these upstreams must be signed by them, everything
  else is denied"
- **You want an image verifier that is not tied to one ecosystem's roadmap**

## When not to use it

- **You only use Cosign and are all-in on Sigstore.** The reference implementation is
  [`../sigstore-policy-controller/README.md`](../sigstore-policy-controller/README.md), and it
  will track the Sigstore specification more closely — particularly for attestation policy, where
  it has CUE and Rego and Connaisseur is thinner
- **Kyverno is already running.** In this repository it is. `verifyImages` covers the common case
  without a second webhook in the pod-creation path — [`../README.md`](../README.md) section 7
- **Gatekeeper is your policy engine and you want verification as an input to it.** That is
  [`../ratify/README.md`](../ratify/README.md)
- **Complex policy over attestation contents.** If the requirement is "the SLSA provenance must
  name this repository and this branch", policy-controller expresses that more directly
- **Nothing is signed yet.** Start at `security/0-governance/supply-chain/signing-artifacts/`

## Notes

Original note recorded for this tool:

- <https://github.com/sse-secure-systems/connaisseur> — the upstream project, from SSE Secure
  Systems. The repository documents the validator types, the image policy syntax (the
  glob-to-validator mapping with a default rule), **detection mode** and **alerting**, and the
  namespaced/cluster-scoped configuration options. The alerting integration is a genuine
  differentiator: it can notify on rejections and on would-be rejections, which is what makes
  detection mode useful rather than just quiet.

From the manifests committed here:

- The chart comes from <https://sse-secure-systems.github.io/connaisseur/charts>, chart
  `connaisseur` version `2.3.2`, in the namespace `connaisseur`.
- The only value overridden is `kubernetes.deployment.replicasCount: 1`. That is a deliberate
  choice for a small cluster and a **liability in a real one**: a single-replica webhook in the
  pod-creation path is a single point of failure, and the interaction with `failurePolicy`
  decides whether its absence blocks the cluster or silently disables enforcement — see
  [`../README.md`](../README.md) section 6.
- The values references kept in the file:
  <https://artifacthub.io/packages/helm/connaisseur/connaisseur> and
  <https://github.com/sse-secure-systems/connaisseur/blob/master/helm/values.yaml>.
- **No validators or image policies are configured**, so as committed it verifies nothing — see
  [`helm/README.md`](helm/README.md).

---

[← Admission control](../README.md)
