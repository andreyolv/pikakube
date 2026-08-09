[← Admission control](../README.md)

# Ratify

<https://github.com/ratify-project/ratify>

Deployment: [`helm/`](helm/README.md)

---

## The problem it solves

Ratify takes a different position from the other verifiers in this folder. It does not own the
policy. It is a **verification engine** whose job is to answer questions about an image's
supply-chain artefacts, and to hand those answers to a policy engine that decides.

The architecture has three parts:

| Part | Role |
|---|---|
| **Referrer store** | discovers artefacts attached to an image digest — signatures, SBOMs, vulnerability reports, licence attestations — using the OCI **Referrers API** |
| **Verifier** | validates a specific artefact type: a Cosign verifier, a Notation verifier, an SBOM verifier, a vulnerability-report verifier |
| **Policy consumer** | Ratify serves the results to **OPA Gatekeeper** as an *external data provider*, and a Rego constraint decides admit or reject |

Why that separation is interesting: it means the admission decision can be about **more than the
signature**. A Gatekeeper constraint can require that the image is signed by Notation *and* has
an SBOM attached *and* that an attached vulnerability report shows no critical findings — all
expressed in the same Rego as the rest of your policy, evaluated by the engine you already
operate.

It is a **CNCF project**, originally from Microsoft, and its natural home is an estate where
Gatekeeper is already the policy engine — Azure Policy for AKS being the obvious example, since
that is Gatekeeper underneath.

## When to use it

- **Gatekeeper/OPA is already the policy engine.** This is the decisive condition. Ratify plugs
  into it as external data; without Gatekeeper it has no decision-maker
- **Admission policy must combine several kinds of evidence** — signature plus SBOM plus
  vulnerability report — in one rule, rather than "is it signed"
- **Notation / Notary v2 signing.** Ratify's Notation support is first-class, reflecting its
  Azure lineage
- **You want verification results reusable outside admission.** Because Ratify is an external
  data provider rather than a webhook, the same verification can feed other policy decisions
- **The OCI Referrers API is how your registry associates artefacts**, which is the modern,
  standardised alternative to Cosign's tag-based convention

## When not to use it

- **You do not run Gatekeeper.** Then you need both Gatekeeper *and* Ratify to get what
  policy-controller or Connaisseur give you in one component. That is a poor trade
- **Kyverno is your policy engine** — as it is in this repository. Kyverno's `verifyImages`
  already does signature and attestation verification natively, and Kyverno and Gatekeeper are
  alternatives, not companions
- **Your registry does not support the Referrers API.** Fallback mechanisms exist, but the
  architecture assumes referrers; older registries make it awkward
- **You want the simplest possible thing that verifies a Cosign signature.** That is
  [`../sigstore-policy-controller/README.md`](../sigstore-policy-controller/README.md), in one
  component
- **Without checking the project's current direction first.** See the note below

## Notes

Original note recorded for this tool:

- <https://github.com/ratify-project/ratify> — the upstream project, now under the
  `ratify-project` organisation after moving out of Microsoft's namespace and into CNCF. The
  repository documents the plugin model (referrer stores and verifiers), the Gatekeeper external
  data integration, the CRDs (`Store`, `Verifier`, `KeyManagementProvider`, `Policy`) and the
  `ratify verify` CLI for testing a policy outside the cluster.

Two things to establish before adopting it, because they decide whether it fits at all:

- **Ratify has been through significant architectural change**, including work on a v2 that
  changes how it is consumed. Check the current release notes and the state of the Gatekeeper
  external-data integration in the version you would deploy, rather than assuming the model
  described in older blog posts still holds.
- **It is not standalone.** Nothing in this folder's manifests deploys Gatekeeper, and without a
  policy engine consuming its output Ratify verifies nothing that anyone acts on.

From the manifests committed here:

- The chart comes from <https://ratify-project.github.io/ratify>, chart `ratify` version
  `1.14.0`, in the namespace `ratify`, with no values overridden.
- The values references kept in the file:
  <https://artifacthub.io/packages/helm/ratify/ratify> and
  <https://github.com/ratify-project/ratify/blob/dev/charts/ratify/values.yaml>.

---

[← Admission control](../README.md)
