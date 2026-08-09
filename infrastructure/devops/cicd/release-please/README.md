[← CI/CD](../README.md)

# release-please

<https://github.com/googleapis/release-please>

---

## The problem it solves

Cutting a release is a sequence of small chores nobody wants to own: decide the next version, work
out what changed since the last tag, write that into a CHANGELOG in a form a human can read, tag the
commit, and publish. Done by hand it is inconsistent; done by a script on every merge it is noise.

release-please derives all of it from the commit history, on one condition: the commits follow
**[Conventional Commits](../../version-control/git/README.md)**. `fix:` is a patch, `feat:` is a
minor, `BREAKING CHANGE:` is a major. The commit messages stop being prose for humans and become
**machine-readable input** — which is the chain
[`version-control/`](../../version-control/README.md#7-conventions-that-are-worth-enforcing) already
describes.

The mechanism that makes it different from a tag-on-merge script is the **release pull request**:

1. Commits land on the default branch as normal
2. release-please opens — and then keeps updating — a pull request that contains the computed version
   bump and the generated CHANGELOG entries
3. That pull request accumulates as more changes merge. It is not one PR per release attempt; it is
   one PR that represents "the release as it currently stands"
4. Merging it is the act of releasing. On merge, the tag and the release are created

| | Tag on every merge | **Release PR** |
|---|---|---|
| The release decision | implicit — merging code released it | explicit — a separate, reviewable merge |
| Version number | computed and applied immediately | computed and **visible before it is real** |
| Changelog | generated after the fact, if at all | generated into a diff you can read and edit |
| Releasing several changes together | not possible; each merge is a version | natural — the PR accumulates |
| Reverting a bad release decision | a published tag exists already | close the PR |

The reviewable-release property is the whole argument. Before anything is published, there is a diff
showing the next version and every line that will appear in the changelog — which is also the moment
somebody notices that a change described as `fix:` is actually breaking.

## When to use it

- a repository that produces a **versioned, released artefact**: a library, a CLI, a container image
  consumed by others, a Helm chart
- when the team already uses Conventional Commits, or is willing to enforce them
- a **monorepo publishing several packages**, which is the case it handles well — per-package
  versions, per-package changelogs, and a release PR that covers only the packages that changed
- when the changelog matters to someone outside the team, and "read the commit log" is not an
  acceptable answer
- when release cadence should be a decision rather than a side effect of merging

## When not to use it

- **without enforcing commit format.** This is the hard dependency, and the failure is quiet: commits
  that do not match the convention are simply not counted, so a release containing three fixes and a
  breaking change is computed as no bump at all. The version numbers become fiction and nobody finds
  out until a consumer upgrades. `commitlint` in a hook and in CI is not optional here — see
  [`version-control/git/`](../../version-control/git/README.md)
- on a repository that is not released. A repository of manifests reconciled from the default branch
  has no version to compute
- as a deployment tool. It tags a source repository; it does not put anything into a cluster
- when releases are calendar-driven and unrelated to what changed. Deriving a version from commit
  types is the point, and forcing it into a fixed schedule loses that
- when the team wants full manual control over the changelog text. Entries can be edited in the
  release PR, but the generated shape is the default and fighting it constantly is a sign of a
  mismatch

## Notes

**The boundary with image update automation is the one to get right.** Two questions look similar and
are not:

| Question | Answered by |
|---|---|
| *What version is this source code?* | release-please — computes the bump, writes the CHANGELOG, tags |
| *Which version is running in the cluster?* | [`image/update/`](../../image/update/README.md) — Flux's image automation writes a new tag into a manifest in Git |

They meet at exactly one point: release-please produces the tag, CI builds and pushes an image
carrying it, and
[flux-image-update](../../image/update/flux-image-update/README.md) notices that tag in the registry
and updates the deployment. Neither tool knows about the other, and neither should. Wiring
release-please directly at a cluster would be push-based CD, which is the thing
[`platform-engineering/gitops/`](../../../platform-engineering/gitops/README.md) exists to avoid.

**Where this fits in pikakube: it mostly does not, and that is worth saying rather than inventing
relevance.** This repository is a collection of manifests reconciled by Flux, not released software.
There is no artefact here with a semantic version, so there is nothing for release-please to compute.
The natural targets are elsewhere — a **Helm chart repository**, or an **application repository**
whose images this platform runs. If a chart or an application repository is added later, this is the
tool for its release process; for this repository, it is mapped rather than applicable.

**Two operational points.** It runs as a GitHub Action or a GitHub App, so it lives beside the rest
of [`github-actions/`](../github-actions/README.md) rather than being separate infrastructure. And
because the entire behaviour is driven by commit messages, the adoption order is fixed: enforce
Conventional Commits first, let a few weeks of history accumulate under the convention, then turn
release-please on. Installed before the convention is enforced, its first release PR proposes a
version derived from commits that were never written to be parsed — and the resulting number is one
nobody should trust.

---

[← CI/CD](../README.md)
