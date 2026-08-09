[← Admission control](../README.md)

# Sigstore policy-controller

<https://github.com/sigstore/policy-controller>

Deployment: [`helm/`](helm/README.md)

---

## The problem it solves

policy-controller is the **reference implementation** of image verification at admission for the
Sigstore ecosystem. If you sign images with Cosign, this is the component built by the same
project to check them.

It installs a validating (and mutating) webhook and introduces one central resource, the
`ClusterImagePolicy`, which says: for image references matching this glob, require signatures or
attestations from this authority.

What a policy can require:

| Requirement | Detail |
|---|---|
| **Key-based signature** | verify against a specific public key |
| **Keyless signature** | verify a Fulcio certificate whose OIDC issuer and subject match — for example a GitHub Actions workflow identity |
| **Rekor transparency log inclusion** | the signing event must be publicly recorded |
| **Attestations** | require a SLSA provenance, SBOM or custom attestation to exist |
| **Policy over attestation contents** | evaluate the attestation payload with **CUE** or **Rego** — for example, "the provenance must name this repository and the `main` branch" |
| **Static allow/deny** | escape hatches for images that will never be signed |

Two behaviours worth knowing before deploying it:

- **Namespace opt-in.** Enforcement applies only to namespaces labelled
  `policy.sigstore.dev/include: "true"`. That is a good default: it makes an incremental rollout
  the natural path rather than something you have to engineer.
- **Digest resolution.** The controller resolves tags to digests and can pin them into the pod
  spec, which closes the race described in [`../README.md`](../README.md) section 2. Confirm this
  is on; verifying a mutable tag is verification with a hole in it.

## When to use it

- **Cosign is your signing tool and Sigstore is the model.** This is the canonical
  implementation, tracks the specification closely, and is the one whose behaviour matches the
  documentation you will be reading
- **Keyless signing with workflow identities.** Requiring that an image was signed by
  `https://github.com/org/repo/.github/workflows/release.yaml@refs/heads/main` is the strongest
  practical control in this folder, and policy-controller expresses it directly
- **Policy over attestation contents.** CUE and Rego over a SLSA provenance predicate is where
  this goes beyond "is it signed" into "was it built the way we build things"
- **You want a namespace-scoped, incremental rollout** without inventing the mechanism yourself
- **Verifying upstream signed images** — distroless, Chainguard, CNCF project images — which is
  a low-friction first policy

## When not to use it

- **Kyverno is already deployed and `verifyImages` is enough.** In this repository Kyverno is
  running. Another webhook in the pod-creation path is a real operational cost; check whether the
  policy engine you already run covers the requirement first — [`../README.md`](../README.md)
  section 7
- **You need Notary v1 (Docker Content Trust) as well.** policy-controller is Sigstore-only; see
  [`../connaisseur/README.md`](../connaisseur/README.md)
- **Gatekeeper/OPA is the policy engine and you want verification as a policy input.** That is
  [`../ratify/README.md`](../ratify/README.md)'s model
- **Nothing is signed yet.** Verification of unsigned images produces either a broken cluster or
  a policy that allows everything. Start at `security/0-governance/supply-chain/signing-artifacts/`
- **Air-gapped, without planning for it.** Keyless verification reaches out to Fulcio and Rekor.
  It can be mirrored or run against a private Sigstore deployment, but that is a project, not a
  flag

## Notes

Original note recorded for this tool:

- <https://github.com/sigstore/policy-controller> — the upstream project, part of the Sigstore
  organisation alongside Cosign, Fulcio and Rekor. The repository documents the
  `ClusterImagePolicy` schema, the namespace opt-in label, the CUE and Rego policy formats for
  attestation evaluation, and the `TrustRoot` resource used to point verification at a private
  Sigstore instance.

From the manifests committed here:

- The chart comes from <https://sigstore.github.io/helm-charts>, chart `policy-controller`
  version `0.10.2`, released into the namespace `sigstore-policy-controller` with the release
  name `policy-controller`.
- The values references kept in the file:
  <https://artifacthub.io/packages/helm/sigstore/policy-controller> and
  <https://github.com/sigstore/helm-charts/blob/main/charts/policy-controller/values.yaml>.
- **No `ClusterImagePolicy` is committed.** The chart installs the controller and its webhook;
  with no policy resource and no namespace carrying the opt-in label, it verifies nothing. The
  policy is the part that does the work — see [`helm/README.md`](helm/README.md).

---

[← Admission control](../README.md)
