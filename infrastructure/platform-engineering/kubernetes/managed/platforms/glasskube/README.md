[← Platforms](../README.md)

# Glasskube

<https://github.com/glasskube/glasskube>

---

## The problem it solves

Glasskube set out to be a package manager for Kubernetes with the property Helm lacks: **dependency
resolution**. Install a package, and the packages it depends on are installed too, at compatible
versions — the model `apt` and `brew` use, rather than Helm's "each chart bundles or assumes its
dependencies".

It shipped as a CLI plus a GUI, with a curated package catalog and an in-cluster operator to
reconcile installed packages.

## When to use it

- Nothing here supports a recommendation — verify the project's current status first
- The dependency-resolution idea remains the interesting part, wherever it ends up living

## When not to use it

- As a platform dependency without checking the repository is active
- On a GitOps cluster, where package installation should originate in Git
- Where Helm plus Flux already covers installation; the gap Glasskube fills is real but narrow

## Notes

Recorded as a link only, with **no chart and no manifests** — one of two entries in this folder with
nothing deployed.

**Check the project's activity before doing anything with it.** Glasskube was a young venture-backed
project, and its direction has shifted; treat the link as a bookmark to verify rather than as a
recommendation. Building on a package manager that stops being maintained is a particularly bad
outcome, because the packages it installed are then managed by nothing.

**The idea is worth keeping even if the tool is not.** Helm genuinely has no dependency resolution
across releases: `dependencies:` in a chart vendors subcharts into it, which is bundling, not
resolution. Installing chart A and chart B that both need cert-manager gives you either two
installations or a manual step. Every platform team solves this the same way in the end — an ordered
list of "install these first", encoded in a GitOps repository — which is exactly what this repository
does with Flux dependencies.

So the honest position: the problem is real, the current answer is dependency ordering in GitOps, and
a package manager that solved it properly would be an improvement. Whether this is that package
manager is not established here.

---

[← Platforms](../README.md)
