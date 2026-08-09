[← Signing artifacts](../README.md)

# Notary

<https://github.com/notaryproject/notary>
<https://github.com/notaryproject/notation>
<https://github.com/notaryproject/specifications>
<https://github.com/theupdateframework/python-tuf>

---

## The problem it solves

The same problem [cosign](../cosign/README.md) solves — proving an artefact came from an
expected publisher and has not been altered — approached from X.509 rather than from Sigstore.

There are two distinct things called Notary and conflating them causes most of the confusion
here:

| | **Notary v1** | **Notary Project / `notation`** |
|---|---|---|
| Status | **largely superseded** | the current work |
| Built on | TUF (The Update Framework) | an OCI-native signature specification |
| Where it shows up | underneath [Docker Content Trust](../docker-trust/README.md) | new deployments, Azure/ACR, Harbor |
| Trust root | per-repository TUF keys | **X.509 — your CA, your HSM** |
| Ergonomics | poor; per-repository root keys, awkward in CI | conventional certificate handling |

The thing Notation offers that cosign does not is a trust root you already own. Signatures
chain to a normal X.509 CA — a corporate PKI, an HSM-backed key, a managed cloud CA — rather
than to Sigstore's Fulcio. For organisations whose certificate policy is already written and
already audited, that is the deciding property.

TUF, listed in the notes as `python-tuf`, is a separate and more general idea: a specification
for securing **software update systems** against attacks that signing alone does not cover —
rollback to an old vulnerable version, freeze attacks where a client is kept from noticing new
releases, and compromise of individual signing roles. It underpins Notary v1, and it is worth
knowing as a concept even where the implementation is not used.

## When to use it

- signatures must chain to an **existing corporate PKI or HSM**, and Sigstore's trust root is
  not acceptable
- an **air-gapped** environment where Fulcio and Rekor are unreachable and self-hosting
  Sigstore is not wanted
- signing events must not be published to a public transparency log
- the registry or platform is built around Notation — Azure Container Registry and Harbor
  integrate with it directly
- you are maintaining an existing Docker Content Trust deployment and are looking at where it
  goes next; Notation is the migration target

## When not to use it

- as the default for a new project on hosted CI — cosign with keyless signing is simpler, has
  a much wider verifier ecosystem, and removes key management rather than reorganising it
- expecting the same attestation coverage — cosign carries SBOMs, SLSA provenance and
  arbitrary in-toto predicates as a first-class feature; Notation is focused on signatures
- **Notary v1 for anything new** — it is what Docker Content Trust runs on, and it is not the
  direction
- if the verifying admission controller only supports cosign, which several do. Check the
  verifier before choosing the signer

## Notes

Original references recorded for this tool:

> <https://github.com/notaryproject/notary>
> <https://github.com/notaryproject/specifications>
> <https://github.com/notaryproject/notation>
> <https://github.com/theupdateframework/python-tuf>

Four links covering three distinct things, which is exactly why this area is confusing.

**`notaryproject/notary`** is v1 — the TUF-based server and client. Recorded here because it
is what you will find running underneath existing Docker Content Trust setups, not because it
is a choice to make today.

**`notaryproject/notation`** is the current CLI, and **`notaryproject/specifications`** is the
part worth reading if you care about interoperability: it defines how a signature is stored as
an OCI artefact referring to the signed image, which is what allows a signature to travel
between registries and be verified by anything implementing the spec. That specification is a
CNCF effort and is the substantive contribution here — the CLI is one implementation of it.

**`theupdateframework/python-tuf`** is the reference implementation of TUF, a different layer
of the problem. TUF's contribution is defending an *update system*, not an artefact: separate
signing roles with separate keys so that compromising one does not compromise the repository,
expiring metadata so a client notices when it is being starved of updates, and version
information so rollback to a known-vulnerable release is detectable. Its ideas show up
throughout this folder — Sigstore uses TUF for its own root of trust — and PyPI's security
work is built on it.

The practical summary for anyone arriving at this folder: if you are choosing, the real
comparison is **cosign vs Notation**, and the question is whose trust root you want. Everything
else on this page is context for systems that already exist.

---

[← Signing artifacts](../README.md)
