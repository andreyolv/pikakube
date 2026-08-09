[← Backend as a service](../README.md)

# Supabase

<https://github.com/supabase/supabase>
<https://github.com/supabase-community/supabase-kubernetes>

---

## The problem it solves

Supabase is the open-source answer to Firebase, and its design decision is the one that makes it
worth having: **it is PostgreSQL, and everything else is a layer on top of it.**

Firebase gives you a proprietary document store. Supabase gives you a real relational database
with real SQL, real constraints and real transactions, and then assembles the rest of the backend
around it:

| Component | What it does |
|---|---|
| PostgreSQL | the actual database — not an abstraction over one |
| PostgREST | a REST API **generated from the schema**; a new table is a new endpoint |
| GoTrue | authentication — email, password, OAuth providers, JWT issuance |
| Realtime | subscriptions to row changes, over websockets |
| Storage | file storage with permissions expressed the same way as table permissions |
| Studio | the web console — schema editor, SQL editor, user management |
| imgproxy | on-the-fly image transformation |
| Kong | the gateway everything is routed through |

The practical effect: for an application that is tables, forms, logins and uploads, most of the
backend does not need to be written. The schema is the API.

The strategic effect, and the reason to prefer it over the hosted alternatives: **the data is in
PostgreSQL**. If Supabase is dropped, the database is still a database, readable by every tool
that speaks Postgres. That is a genuinely different exit cost from a proprietary document store.

## When to use it

- **CRUD-shaped applications** — tables, forms, authentication, file uploads. This is the case it
  is built for and it is very good at it.
- Prototypes and internal tools, where the cost of writing an API service is most of the cost of
  the project.
- When authentication with several providers is needed and nobody wants to build it.
- Self-hosted, when **the data must stay in the cluster** — data location is the main honest
  reason to self-host rather than use the hosted service.
- With [row-level security designed first](../README.md#5-the-authorisation-model-is-the-real-decision).
  Clients talk to PostgREST directly, so policies are the security model, not a refinement of it.

## When not to use it

- When the application's value is **between the request and the row** — workflows, orchestration,
  domain rules. A generated API becomes something to work around, endpoint by endpoint. Write the
  service instead.
- As a general-purpose PostgreSQL for other workloads. It is a bundled database with a specific
  lifecycle, and the repository already runs PostgreSQL properly with operators — see
  [`../../../databases/sql/postgresql/`](../../../databases/sql/postgresql/README.md).
- Self-hosted, to save money. It is eight or nine components with one name; the saving is not the
  reason.
- Self-hosted, without deciding who upgrades it. The supported self-hosting path upstream is Docker
  Compose; the Kubernetes chart is community-maintained.
- With the demo credentials in place. See the notes.

## Notes

### Recorded links

| Link | What it is |
|---|---|
| <https://github.com/supabase/supabase> | the project |
| <https://github.com/supabase-community/supabase-kubernetes> | the **community** Helm chart — what the deployment here uses |

The second link carries the caveat that matters: `supabase-community` is not `supabase`. The
officially supported self-hosting path is Docker Compose, and the Kubernetes chart is a community
effort. It works, and it is the only reasonable option for a GitOps cluster — but it is not
covered by upstream's support or upstream's release testing.

### What is deployed here

Three manifests, all Flux:

| File | Contents |
|---|---|
| `namespace.yaml` | the `supabase` namespace |
| `helm/gitrepository.yaml` | a `GitRepository` in `flux-system` pointing at `supabase-community/supabase-kubernetes`, branch `main`, with an `ignore` block that excludes everything except `/charts/supabase` |
| `helm/helmrelease.yaml` | the `HelmRelease`, 5m interval, chart path `charts/supabase` from that `GitRepository` |

The `ignore` block is a good detail worth keeping: Flux clones only the chart directory instead of
the whole repository, which keeps the source small and the reconciliation fast.

### The version problem

The `GitRepository` tracks `ref.branch: main`. There is no chart version and no tag.

That means **the chart moves when upstream moves**, and Flux applies it on the next reconciliation.
For a nine-component stateful application — with a database in it — that is the riskiest available
upgrade policy: an upstream commit becomes a production change with no review step.

Pinning to a tag or a commit is the fix, and the contrast is in this repository already:
[SonarQube](../../code-quality/static-analysis/sonarqube/README.md) pins its chart to `2026.3.1`.

### The values are the upstream example

The `HelmRelease` carries the values from
[the chart's own `values.yaml`](https://github.com/supabase-community/supabase-kubernetes/blob/main/charts/supabase/values.yaml),
which the file links to in a comment. They are demo values and are not usable as they stand:

| Value | What is there |
|---|---|
| `secret.jwt.anonKey` / `serviceKey` | `xxxxxxxxxxxxxxxxx` — placeholders |
| `secret.jwt.secret` | `your-super-secret-jwt-token-with-at-least-32-characters-long` |
| `secret.dashboard.password` | `this_password_is_insecure_and_should_be_updated` |
| `secret.db.password`, `smtp.password` | `example123456` |
| `secret.analytics.apiKey` | `your-super-secret-and-long-logflare-key` |
| URLs | `http://example.com` for `SUPABASE_PUBLIC_URL`, `API_EXTERNAL_URL`, `GOTRUE_SITE_URL` |

**Every one of those is a secret in Git.** Before this runs anywhere real they need generating and
moving into SOPS or an External Secret. The JWT secret is the important one: `anonKey` and
`serviceKey` are signed with it, and the service key bypasses every row-level security policy.

Other values recorded in the release, which are real configuration decisions rather than
placeholders:

| Setting | Value | Note |
|---|---|---|
| `db.persistence.size` | 1Gi | demo-sized; this is the system of record for everything |
| `storage.persistence.size`, `imgproxy.persistence.size` | 1Gi each | same |
| `studio.image.tag` | `20240326-5e5586d` | pinned |
| `auth.image.tag` | `v2.143.0` | pinned |
| `GOTRUE_MAILER_AUTOCONFIRM` | `"true"` | **email confirmation disabled** — fine for a demo, wrong for anything with real users |
| `GOTRUE_EXTERNAL_EMAIL_ENABLED` | `"true"` | email sign-up on |
| SMTP | `smtp.example.com:587` | not configured |
| `vector` | mounts the node's `/var/log/pods` via `hostPath` | log collection reads pod logs off the host — a privileged read of every pod's output on that node |

That last row is worth flagging: the analytics component collects logs by mounting the node's log
directory. It is how the upstream chart works, and it means the Supabase namespace can read the
logs of every pod scheduled on the same node.

### Summary of state

Mapped, not running: Flux manifests exist, the chart is community-maintained and unpinned, and
every credential is a placeholder. The three things to do before it is real — **pin the chart,
replace the secrets, size the volumes** — are all in the same file.

---

[← Backend as a service](../README.md)
