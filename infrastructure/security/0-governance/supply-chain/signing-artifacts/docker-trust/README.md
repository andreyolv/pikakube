[← Signing artifacts](../README.md)

# Docker Content Trust

<https://docs.docker.com/engine/security/trust/>

---

## The problem it solves

Docker Content Trust (DCT) was Docker's built-in image signing: set `DOCKER_CONTENT_TRUST=1`
and `docker push` signs the image, `docker pull` refuses anything unsigned. It is built on
[Notary v1](../notary/README.md) and TUF, with per-repository root and targets keys.

It solved the right problem at a time when nothing else did, and it is **legacy**. Anything
new should use [cosign](../cosign/README.md), or [Notation](../notary/README.md) if the trust
root must be an existing PKI.

The reasons it lost, stated concretely rather than as a preference:

| Problem | Consequence |
|---|---|
| **Opt-in via an environment variable** | `DOCKER_CONTENT_TRUST` unset means signing and verification silently do not happen. A control that is off by default and fails open is not much of a control |
| Per-repository root keys | key ceremony and key custody per repository; painful at any scale, and the recovery story for a lost root key is "you cannot" |
| Poor CI ergonomics | passphrases and key files in a pipeline, with no OIDC or identity-based path |
| No attestation support | signatures only — no SBOM, no provenance, no in-toto predicates |
| Tied to the Docker CLI | does not fit BuildKit-only, buildah, ko or Kaniko builds, and not to Kubernetes admission |
| Effectively frozen | Notary v1 is superseded; the ecosystem's verifiers target cosign |

## When to use it

- **maintaining an existing deployment** that already depends on it, where the alternative is
  a migration nobody has scheduled
- a Docker Hub or Docker Trusted Registry setup where DCT is already the established mechanism
  and the consumers already have the trust data
- understanding what a system in front of you is doing, which is the most likely reason to read
  this page

## When not to use it

- **anything new** — cosign for the general case, Notation where a corporate PKI is the root
- Kubernetes admission control — the verifiers in `3-container/admission/` speak cosign and
  Notation signatures, not DCT
- pipelines that do not build with the Docker CLI, which is most modern ones
- when SBOM or provenance attestations are also needed — DCT has no concept of them
- when signing must be enforced rather than opted into; the environment-variable model makes
  "we sign our images" true only where someone remembered to set it

## Notes

Original reference recorded for this tool:

> <https://docs.docker.com/engine/security/trust/>

The official documentation, and it is worth reading for one reason beyond history: it explains
the **TUF key hierarchy** — offline root key, repository targets key, delegation keys,
timestamp and snapshot keys — clearly, and that hierarchy is the same idea that reappears in
Notary Project and in Sigstore's own root of trust. The mechanism is sound; the packaging is
what did not survive.

If you encounter DCT in an existing system, two practical points. First, the trust data lives
in a Notary server separate from the registry, so a registry migration that does not carry the
trust data silently breaks verification. Second, `DOCKER_CONTENT_TRUST=1` set in one place and
not another produces the worst possible outcome — an inconsistent estate where some pulls are
verified and nobody can say which — so the migration path is usually to turn it off
deliberately and adopt admission-time verification instead of leaving it half-enabled.

---

[← Signing artifacts](../README.md)
