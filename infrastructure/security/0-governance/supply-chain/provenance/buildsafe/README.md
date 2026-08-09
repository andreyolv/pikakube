[← Provenance](../README.md)

# BuildSafe

<https://github.com/buildsafedev/bsf>
<https://github.com/chainloop-dev/chainloop>

---

## The problem it solves

The SLSA levels describe what a trustworthy build looks like, and then leave you to get there
with the build system you already have — which is usually a Dockerfile that runs
`apt-get install` against whatever the mirror serves today. Provenance emitted from such a
build is accurate about the steps and says nothing useful about the inputs, because the inputs
were not controlled.

The two projects recorded in this folder attack that from opposite ends.

**`bsf` (BuildSafe)** approaches it from the build itself. It uses Nix as the substrate to
produce container images with declared, pinned inputs — hermetic by construction rather than
by discipline. The consequence that matters here: when every input is declared, the SBOM is
exact rather than inferred, and the provenance describes a build that genuinely could not have
fetched anything else. It is the same argument as the `3-container/base-images/` tooling — apko, melange, Wolfi —
arrived at from the Nix direction.

**Chainloop** approaches it from the evidence side. It is a CNCF Sandbox project that acts as
an attestation control plane: pipelines send their evidence — SBOMs, provenance, test results,
scan output — through a single contract-driven service, which validates that a workflow
produced the evidence it was required to produce, signs it, and stores it in one place. It
answers a question none of the individual tools do: *did every release actually emit the
evidence policy says it must?*

## When to use it

**bsf**, when:

- hermetic builds are the goal and the team is willing to accept Nix as the build substrate
- exact SBOMs matter more than familiarity — declared inputs remove the guesswork that
  scanning-based inventories have to do
- minimal images are wanted for the same reasons as distroless/Wolfi, and Nix is already in
  use somewhere (this repository uses devbox, which is Nix underneath)

**Chainloop**, when:

- several teams and several pipelines produce evidence and nobody can say whether all of them
  did
- the requirement is *policy over the pipeline's outputs* — "every release must carry an SBOM
  and a provenance attestation" — enforced centrally rather than reviewed by hand
- evidence needs a single durable home with an audit trail, separate from CI retention

## When not to use it

- expecting either to be the standard path. `slsa-github-generator` and `actions/attest` cover
  the mainstream case with far less adoption cost — see [`slsa/`](../slsa/README.md)
- **bsf** if Nix is not acceptable. The learning curve is the real cost and it is paid by
  everyone who touches the build, not just the person who set it up
- **Chainloop** with a single pipeline. Its value is aggregation and conformance across many;
  with one workflow it is a service in front of a file
- either one before provenance is being produced at all. These improve or govern a practice
  that has to exist first

## Notes

Original references recorded for this folder:

> <https://github.com/buildsafedev/bsf>
> <https://github.com/chainloop-dev/chainloop>

Two projects filed together under provenance, and it is worth being explicit that they are not
alternatives to each other — they sit at different points of the same pipeline. `bsf` changes
**how the artefact is built** so that strong claims are true; Chainloop changes **what happens
to the claims** once made. A shop could reasonably run both, or neither.

Both are early relative to the rest of this folder. `bsf` is a small project and the Nix
dependency is a hard prerequisite rather than an implementation detail; Chainloop is CNCF
Sandbox, which is the earliest CNCF stage. Neither should be read as a default, and both are
recorded here because they represent directions worth knowing about: hermeticity as a build
property, and attestation conformance as a control plane.

The general principle behind `bsf` is the one worth taking away even if the tool is not
adopted: **provenance is only as meaningful as the build's control over its inputs.** A
non-hermetic build produces honest provenance about a process that could have pulled anything.
That is why hermeticity appears in the SLSA discussion at all, and why the base-image work in
`3-container/` is closer to this folder than the folder structure suggests.

---

[← Provenance](../README.md)
