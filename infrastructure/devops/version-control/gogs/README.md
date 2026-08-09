[← Version control](../README.md)

# Gogs

<https://github.com/gogs/gogs>

---

## The problem it solves

**The original tiny self-hosted forge.** Gogs — "Go Git Service" — is a single binary with very
low resource requirements: repositories, pull requests, issues and a wiki, running comfortably on
hardware where nothing else in this folder would.

| Property | Detail |
|---|---|
| Single binary | no runtime dependencies, cross-platform |
| **Very small footprint** | it genuinely runs on a Raspberry Pi |
| Database | SQLite, PostgreSQL, MySQL or TiDB |
| Authentication | local, LDAP, SMTP, PAM |
| Webhooks and an API | present, and modest |
| Migration | pull mirrors from other forges |

What it does not have, and this is the honest list: no CI, no package registry, no Actions
compatibility, no OIDC, and a much smaller feature surface than [Gitea](../gitea/README.md) —
because almost everything in that list is post-2016, and post-fork.

## When to use it

- **the smallest possible forge on very constrained hardware**, where even Gitea is too much
- a personal Git server where the requirement really is repositories and nothing else
- an existing Gogs installation that works and has no reason to move

## When not to use it

- **as a new deployment** — [Gitea](../gitea/README.md) is the maintained continuation of this
  same project and is better in nearly every respect
- where CI, a package registry or modern authentication are wanted
- where the release cadence and the size of the community matter
- **as the source of a GitOps repository** — [§4 of the parent](../README.md#4-the-gitops-consequence)
  applies, and on a project this quiet the availability argument is weaker still

## Notes

Recorded link:

- <https://github.com/gogs/gogs> — the project.

**Gogs is the ancestor; [Gitea](../gitea/README.md) is the fork that took over.** In late 2016 a
group of contributors forked Gogs into Gitea, over the pace of development and the single-
maintainer bottleneck that came with it. What followed is not close: Gitea accumulated the great
majority of the contributors, the releases and the features — Actions-compatible CI, a package
registry, a project-maintained Helm chart — while Gogs continued at a much quieter pace.

Stated carefully, because "dead" would be wrong: **Gogs is not abandoned.** It still receives
commits and releases, and it still does what it always did. It is markedly quieter, has a small
fraction of the surrounding ecosystem, and has not followed the feature expansion that makes Gitea
a current choice.

The practical conclusion: **choosing Gogs over Gitea today needs a specific reason**, and the only
one that really holds is extreme resource constraint. For everything else, the fork is the answer,
and it is the one this repository maps with a working `HelmRelease`.

Nothing is deployed here — this folder holds the reference and no manifests, which is consistent
with that conclusion.

## Where it fits here

Documented in [`version-control/`](../README.md) for completeness and for the history, because the
Gogs-to-Gitea relationship is the single most useful fact when comparing the small self-hosted
forges — and it is easy to evaluate them as two equivalent options when they are not.

[Gitea](../gitea/README.md) is the one mapped as a deployment, and it is the right default.

---

[← Version control](../README.md)
