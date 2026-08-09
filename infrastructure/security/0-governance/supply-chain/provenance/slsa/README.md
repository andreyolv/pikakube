[← Provenance](../README.md)

# SLSA

<https://github.com/slsa-framework/slsa>
<https://github.com/slsa-framework/slsa-github-generator>
<https://github.com/actions/attest-build-provenance>
<https://github.com/actions/attest>

---

## The problem it solves

Everyone claims their build pipeline is secure and nobody can say what that means. SLSA
(Supply-chain Levels for Software Artifacts, an OpenSSF project) turns it into a ladder with
defined rungs, so "our builds are trustworthy" becomes a claim with content and a way to check
it.

It is a **framework, not a tool**. There is no SLSA binary to install. You reach a level by
meeting requirements about where and how your builds run, and by emitting signed provenance
that a verifier can check. The format that provenance is written in is
[in-toto](../in-toto/README.md).

The levels in the v1.0 build track:

| Level | Requirement | Rules out |
|---|---|---|
| L1 | provenance exists and is available | nothing on its own — it establishes the plumbing |
| **L2** | provenance is **signed by a hosted build platform** | a human fabricating provenance |
| **L3** | the build platform is hardened and isolated; provenance is unforgeable and build secrets are unreachable from the build | one build tampering with another; a compromised step forging its own provenance |

The practical read: **L2 is a day's work on hosted CI with OIDC.** L3 depends on the build
platform's own guarantees and is not something a repository can configure by itself.

## When to use it

- you build artefacts others consume — images, binaries, libraries — and want the "built from
  that source, by that pipeline" claim to be checkable
- a customer, an auditor or a downstream consumer asks what your build integrity level is;
  SLSA is the vocabulary they will use
- as the **policy target** for verification: an admission rule that requires SLSA provenance
  naming an expected repository and workflow
- to decide where to invest — the level model makes it obvious that hosted, isolated builders
  buy more than any amount of scanning
- when evaluating a dependency: "does upstream publish SLSA provenance" is a real signal

## When not to use it

- as a substitute for signing — provenance and signature answer different questions and you
  want both. See [`signing-artifacts/`](../../signing-artifacts/README.md)
- expecting it to say anything about the **code**. SLSA is about the integrity of the build,
  not the quality or safety of what was built. A perfectly SLSA L3 build of vulnerable code is
  perfectly SLSA L3
- as a badge. Claiming a level without meeting the requirements is worse than claiming
  nothing, because others make decisions on it
- as the first supply-chain investment for a team with no CI hygiene at all — pinned actions,
  scoped tokens and a hardened runner come first, and they are cheaper

## Notes

Original notes recorded for this tool, translated:

> <https://github.com/slsa-framework/slsa>
>
> only for public repositories
> <https://github.com/slsa-framework/slsa-github-generator>
>
> for private repositories
>
> the legacy one
> <https://github.com/actions/attest-build-provenance>
>
> the new one
> <https://github.com/actions/attest>

This is a practical routing note and it is the most useful thing on this page.

**`slsa-github-generator` is public-repository only.** It is the SLSA project's own set of
reusable GitHub Actions workflows, and it reaches SLSA L3 by running the build inside a
workflow the calling repository cannot modify — that isolation is exactly what L3 requires.
The restriction follows from the mechanism rather than from licensing: it depends on the
public transparency log and on the reusable-workflow isolation model, so private repositories
are not supported. If the repository is public and the goal is a strong level, this is the
route.

**For private repositories, GitHub's own attestation actions.** `attest-build-provenance` is
the purpose-built one: it generates a signed SLSA provenance attestation for a built artefact
using the workflow's OIDC identity, with no key to manage. `actions/attest` is the more
general successor — the same signing machinery, but able to attest **any** predicate type, not
just provenance, which means SBOM attestations and custom statements go through the same path.

Calling `attest-build-provenance` "legacy" is a fair reading of the direction rather than a
statement that it is deprecated: it still works and is still the simplest thing for the
provenance-only case. `actions/attest` is where the generality is. For a repository that will
eventually attest both provenance and SBOMs, standardising on the general one avoids running
two mechanisms.

One thing none of these do: **verify**. All three produce attestations. The check that an
attestation exists, is signed by the expected identity, and names the expected source and
workflow happens later — `slsa-verifier` at release time, or a policy in
`3-container/admission/` at deploy time. Producing without verifying is the anti-pattern the
[capability README](../README.md#4-verification-is-the-whole-point) spells out.

---

[← Provenance](../README.md)
