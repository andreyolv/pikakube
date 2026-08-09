[← Toolchain](../README.md)

# Spack

<https://github.com/spack/spack>

---

## The problem it solves

Spack is a package manager for **HPC and scientific computing**, originating at Lawrence Livermore
National Laboratory. Its users are national labs, research computing centres and university
clusters — not application teams.

The problem it exists for is not the one the other tools in this folder solve. It is this: a
scientific application has to be **built from source**, against a *specific compiler*, a *specific
MPI implementation*, and *specific build options* tuned to the hardware it will run on. The same
package must exist in many such builds simultaneously, because different users on the same cluster
need different combinations. That is a build matrix, not a version list.

| Concern | Why the usual tools do not cover it |
|---|---|
| **Compiler choice** | GCC, Clang, Intel, NVIDIA — the same source produces different binaries and different performance |
| **MPI implementation** | OpenMPI vs. MPICH vs. a vendor MPI is not an implementation detail on a cluster |
| **Build variants** | optional features and hardware-specific optimisations, chosen per build |
| **Many builds coexisting** | one machine, many combinations, all installed at once |
| **Building from source is the norm** | binary packages for the exact combination usually do not exist |

Spack's model is a **spec syntax** describing a package together with its version, compiler,
variants and dependencies, and a store where every distinct combination installs to its own path.
The underlying question — declared, reproducible, multi-version software environments — is the
same one [mise](../mise/README.md), [devenv](../devenv/README.md) and [flox](../flox/README.md)
answer. The constituency is completely different.

## When to use it

- **Scientific or HPC software built from source** against a chosen compiler and MPI
- A shared cluster where many users need different builds of the same package at the same time
- Performance depends on build-time options tuned to specific hardware
- The software stack is Fortran, C or C++ with a deep native dependency graph and no usable binary
  distribution
- Research computing environments where this is already the established convention — it is, widely

## When not to use it

- **Application development on Kubernetes** — this is not the problem, and reaching for Spack here
  is a category error
- Pinning CLI tool versions for a repository — that is [mise](../mise/README.md), at a fraction of
  the weight
- Reproducible developer environments generally — [devenv](../devenv/README.md),
  [flox](../flox/README.md) or
  [Devbox](../../../../platform-engineering/kubernetes/local/linux/virtual-enviroment/devbox/README.md)
- Anywhere prebuilt binaries or images are adequate, since building from source is Spack's central
  assumption and its central cost
- Web, cloud or platform stacks — the dependency graphs Spack is designed for are not the ones
  these have

## Notes

**Its relevance to this repository is thin, and that is the honest position.** pikakube is a
Kubernetes platform repository. It has no Fortran, no MPI, no compiler-matrix problem, and no
cluster of researchers needing eleven builds of the same library. Nothing here would be better if
Spack were adopted, and this folder is not going to manufacture a use case for it.

**Why catalogue it anyway.** Two reasons, both practical.

The first is that it completes the map. The three families in
[`toolchain/`](../README.md#3-three-approaches) — version managers, Nix-based environments,
source-building package managers — are three answers to one question, and seeing the third makes
the trade-offs in the other two legible. Nix's reproducibility looks maximal until you see a tool
whose users routinely need *the same package, eleven ways, at once*.

The second is that knowing it exists prevents a specific mistake: someone facing a genuine build
matrix reaching for a container image per combination. Containers isolate; they do not manage a
combinatorial build space, and a container per compiler/MPI/variant tuple is a maintenance problem
that grows multiplicatively. If that problem ever appears — and in a platform serving research or
simulation workloads it might — Spack is the tool that already solves it, and the correct move is
to recognise it rather than reinvent it.

**Where it would plausibly touch a Kubernetes platform**, if it ever did: building images for HPC
or simulation workloads that will run on the cluster, where the image contents need Spack's build
model even though the orchestration does not. That is a hypothetical, not a plan, and nothing in
this repository is close to it.

Spec syntax, subcommands, environment file formats and the details of Spack's compiler and mirror
configuration are not recorded here and are unverified in this repository — read the upstream
documentation.

---

[← Toolchain](../README.md)
