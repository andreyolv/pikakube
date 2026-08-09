[← Signing artifacts](../README.md)

# Cosign

<https://github.com/sigstore/cosign>
<https://github.com/sigstore/cosign-installer>
<https://github.com/sigstore/gh-action-sigstore-python>
<https://github.com/sigstore/rekor>
<https://github.com/sigstore/fulcio>

---

## The problem it solves

A registry will serve whatever was pushed to it. Nothing in a `docker pull` establishes that
the image came from the pipeline you think publishes it, or that it has not been replaced
since.

Cosign signs container images and other OCI artefacts, and stores the signature **in the
registry beside the artefact** — no separate infrastructure, no key distribution channel, no
detached files to lose. It also attaches attestations (SBOMs, SLSA provenance, custom
in-toto predicates), so the same tool covers signatures and evidence.

Its important feature is **keyless signing**: instead of holding a private key, a CI job
exchanges its OIDC identity for a short-lived certificate from Fulcio, signs, discards the key,
and the event is recorded in the Rekor transparency log. Verification then names an *identity*
— "the release workflow on the main branch of this repository" — rather than a key fingerprint.
The mechanics are in [`../README.md`](../README.md#keyless-signing).

It is the de facto standard for OCI signing, and the ecosystem assumes it: the Sigstore policy
controller, Kyverno's `verifyImages`, Connaisseur and Ratify all verify cosign signatures.

## When to use it

- signing **container images**, which is the default case, and there is no serious competitor
- attaching SBOM or provenance attestations to an image so they travel with it in the registry
- CI on a platform with OIDC (GitHub Actions, GitLab, Buildkite) — keyless removes key
  management entirely and makes the verification policy readable
- signing **Helm charts**, since OCI-packaged charts are just OCI artefacts
- signing arbitrary files or release binaries — `cosign sign-blob`
- anywhere the verifier will be a Kubernetes admission controller, because they all speak
  cosign

## When not to use it

- **air-gapped environments**, without self-hosting Fulcio and Rekor — keyless needs both
  reachable at signing time, and self-hosting the Sigstore stack is a real project
- when signing events must stay private — a Rekor entry publicly reveals that a repository
  published something at a given time. Use a private Sigstore instance or key-based signing
- when signatures must chain to an **existing corporate PKI or HSM root** — that is
  [Notation](../notary/README.md)'s case; cosign keyless roots trust in Sigstore
- as the entire supply-chain story. It proves integrity, not that the build was honest — pair
  it with [provenance](../../provenance/README.md)
- if nothing verifies. Signing without verification is a build step with no effect

## Notes

Original notes recorded for this tool, including the commands actually run:

> <https://github.com/sigstore/cosign>
> <https://github.com/sigstore/cosign-installer>
> <https://github.com/sigstore/gh-action-sigstore-python>
>
> <https://github.com/sigstore/rekor>
> <https://github.com/sigstore/fulcio>
>
> LOCAL
> ```bash
> cosign generate-key-pair
> ```
>
> SIGN
> ```bash
> cosign sign --key cosign.key docker.io/andreyolv/flink@sha256:1badb98e146ca63e9c92947dae5c9a0ba535e4bc3f9d57167845f4a3b325510f
> ```
>
> VERIFY
> ```bash
> cosign verify --key cosign.pub docker.io/andreyolv/flink:1.0@sha256:1badb98e146ca63e9c92947dae5c9a0ba535e4bc3f9d57167845f4a3b325510f
> ```

**What these commands do.** `generate-key-pair` writes `cosign.key` (encrypted with a
passphrase) and `cosign.pub`. `sign` computes a signature over the image's digest and pushes it
into the registry as an additional OCI object associated with that digest. `verify` fetches
that object and checks it against the public key, printing the verified payload on success and
failing non-zero otherwise — which is what makes it usable in a script.

**The detail that is correct and often is not.** Both commands address the image by
`@sha256:...`. A signature binds to a digest, never to a tag, so signing or verifying a bare
tag leaves the door open described in
[`../README.md`](../README.md#4-digests-not-tags): the tag can be repointed at an unsigned
image afterwards and the original signature stays perfectly valid. Note that the verify command
carries **both** the tag and the digest (`flink:1.0@sha256:...`) — that form is legal and the
digest is what is authoritative; the tag is decoration.

**The key pair is the part to move.** `generate-key-pair` locally is the right way to learn
the tool and the wrong way to operate it: the private key becomes a file someone must keep
safe, rotation is manual, and there is no record of what it signed. In CI with OIDC the same
signing is done keyless — no key, and verification names the workflow instead of a fingerprint.

**The other repositories in the note.** `cosign-installer` is the GitHub Action that puts the
cosign binary on a runner — the normal way to use it in a workflow.
`gh-action-sigstore-python` is the equivalent for Python **release artefacts** (wheels and
sdists) rather than images: same Sigstore trust model, different artefact type, and the
standard way PyPI packages get signed.

**Fulcio and Rekor** are the two services that make keyless work, and they are worth knowing
by name: Fulcio is the CA that issues the short-lived certificate from an OIDC token, Rekor is
the append-only transparency log that records the signing event so it remains verifiable after
the certificate expires. Rekor also enables a detection capability nothing key-based has —
watching the public log for entries claiming your own identities.

**One operational note not in the original.** Signatures are separate registry objects. Copying
an image between registries with a plain `docker pull`/`push` leaves the signature behind, and
verification then fails downstream for a reason that looks like a bug. Use a copy tool that
carries referrers (`cosign copy`, or `crane`/`skopeo` with the appropriate flags).

---

[← Signing artifacts](../README.md)
