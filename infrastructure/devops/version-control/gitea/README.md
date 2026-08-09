[← Version control](../README.md)

# Gitea

<https://github.com/go-gitea/gitea>
<https://gitea.com/gitea/helm-chart>

---

## The problem it solves

**A self-hosted forge that is a pod and a database.** Gitea is a single Go binary providing
repositories, pull requests, issues, releases, a wiki, a package registry and CI — with an
operational footprint measured in hundreds of megabytes rather than gigabytes.

| Capability | Detail |
|---|---|
| Repositories, pull requests, issues, wiki | the forge basics, complete |
| **Gitea Actions** | CI with **GitHub Actions-compatible** workflow syntax, using `act` runners |
| **Package registry** | OCI/Docker, Helm, npm, PyPI, Maven, and more — one server for code and artefacts |
| Mirroring | pull mirrors from, and push mirrors to, other forges |
| Authentication | local, LDAP, OAuth2, OIDC, SMTP |
| Webhooks | including GitHub-compatible payloads, so integrations often work unchanged |
| Storage | filesystem for repositories; SQLite, PostgreSQL or MySQL for metadata |

Two features change the evaluation more than the feature list suggests. **Actions compatibility**
means existing GitHub workflows frequently run with minimal changes — the migration cost that
usually blocks leaving GitHub. And the **package registry** means a self-hosted Gitea can also be
the OCI registry from [`../../image/oci-registry/`](../../image/oci-registry/README.md), which is
one fewer thing to operate for a small platform.

## When to use it

- **the default self-hosted forge** — it is the one to reach for unless something specific rules it
  out
- where code may not leave the network, or a forge must be under your control
- as an internal mirror of external repositories, for availability
- small teams and homelabs, where GitLab is absurd and a forge is still wanted
- where CI, a package registry and a forge in one modest deployment is attractive

## When not to use it

- **as the source of the GitOps repository on the cluster it deploys** — that circularity is
  [§4 of the parent](../README.md#4-the-gitops-consequence), and it is a real problem
- where the full DevOps-platform feature set is genuinely needed —
  [GitLab](../gitlab/README.md) exists for that
- where the ecosystem matters: GitHub Apps, marketplace integrations and third-party services
  mostly do not exist for Gitea
- where nobody wants to own backups, upgrades and restores; the operational burden is small but
  not zero

## Notes

Recorded link:

- <https://github.com/go-gitea/gitea> — the project.

**Gitea is the maintained fork of [Gogs](../gogs/README.md).** It was forked in late 2016 by
contributors who wanted community governance and a faster release cadence than a single-maintainer
project could sustain. Since then Gitea has taken the overwhelming majority of the activity, and
the features that make it a current choice — Actions, the package registry, a maintained Helm
chart — are all post-fork. Between the two, **Gitea is the answer**; choosing Gogs needs a
specific reason.

For completeness, since it comes up: Gitea was itself forked into **Forgejo** in 2022, after
Gitea's governance moved to a for-profit company. Forgejo is a live project, is what Codeberg
runs, and is not mapped in this repository.

**What is configured here** — a Flux `HelmRelease` at chart version **10.0.2**, in the `gitea`
namespace, with a deliberate set of choices:

```yaml
redis-cluster:  { enabled: false }
postgresql:     { enabled: true }
postgresql-ha:  { enabled: false }
gitea:
  config:
    database: { DB_TYPE: postgres }
    session:  { PROVIDER: db }
    cache:    { ADAPTER: memory }
    queue:    { TYPE: level }
    indexer:
      ISSUE_INDEXER_TYPE: bleve
      REPO_INDEXER_ENABLED: true
```

Read as a set, these say **"single-instance Gitea, minimum moving parts"**:

| Setting | What it decides |
|---|---|
| `redis-cluster: false`, `cache: memory` | no Redis at all — the cache is in-process |
| `session: db` | sessions in PostgreSQL, which is what makes dropping Redis safe |
| `queue: level` | the queue is an embedded LevelDB on disk, not Redis |
| `postgresql: true`, `postgresql-ha: false` | one PostgreSQL, not a replicated pair |
| `ISSUE_INDEXER_TYPE: bleve` | the search index is embedded, not Elasticsearch |
| `REPO_INDEXER_ENABLED: true` | **code search across repositories**, at the cost of an index that grows with the code |

The consequence is that this is a **single-replica** deployment by construction. An in-process
cache, an on-disk queue and an embedded index cannot be shared between replicas. That is the right
trade for a small forge — far fewer components to operate — and it is a ceiling to be aware of
before scaling becomes a question.

**The two things to get right before it holds anything that matters**, both from
[§3 of the parent](../README.md#3-self-hosted-or-saas):

1. **Back up the database, not only the volumes.** The repositories are on disk and recoverable
   from clones; pull requests, issues, reviews, permissions and tokens exist **only** in
   PostgreSQL. Backing up the volume and forgetting the database is the classic self-hosting
   failure, and it is discovered at the worst possible moment.
2. **Have a tested restore**, not a backup job. A backup nobody has restored is a hypothesis.

## Where it fits here

Mapped as the **self-hosted default** in [`version-control/`](../README.md), and not the forge
this repository lives on — which is correct. By
[§4 of the parent](../README.md#4-the-gitops-consequence), a Gitea running on this cluster and
holding this cluster's desired state would be circular: a rebuild could not start, because the
source of truth is one of the things being rebuilt. If that changes, the fix is a push mirror to
an external forge, so Flux always has a surviving source to reconcile from.

Compared with the alternatives: [GitLab](../gitlab/README.md) is an entire DevOps platform and a
serious commitment; [Gitness](../gitness/README.md) trades ecosystem for built-in pipelines;
[Gogs](../gogs/README.md) is the quieter ancestor.

---

[← Version control](../README.md)
