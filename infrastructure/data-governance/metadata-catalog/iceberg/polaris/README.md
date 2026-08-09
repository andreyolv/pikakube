[← Iceberg REST catalogs](../README.md)

# Apache Polaris

<https://github.com/apache/polaris>

<https://github.com/apache/polaris-tools>

---

## The problem it solves

An **Iceberg REST catalog** donated to the Apache Software Foundation by Snowflake — the
implementation with the most weight behind its name, and the reference other implementations get
compared to.

| Property | Detail |
|---|---|
| Origin | Snowflake, donated to the ASF; now Apache Polaris |
| Language | Java (Quarkus) |
| State | a relational database |
| Protocol | the Iceberg REST catalog specification |
| Model | catalogs, principals, principal roles, catalog roles, grants |
| **Credential vending** | supported — the catalog issues scoped, temporary storage credentials |
| Federation | can front an existing catalog, including HMS |
| `polaris-tools` | migration and administration utilities, including a catalog migrator |

The role model is more elaborate than the alternatives: principals hold principal roles, principal
roles are granted catalog roles, and catalog roles hold privileges on namespaces and tables. That
is a real RBAC design rather than an afterthought, and it is what credential vending resolves
against when an engine asks to load a table.

`polaris-tools` is worth knowing about separately. The catalog migrator can bulk-register tables
from one catalog into another, which is the mechanism for moving an
[HMS](../../hms/README.md) estate onto REST without rewriting the data.

## When to use it

- Apache Foundation governance is a requirement — it is the only implementation here with a
  vendor-neutral foundation *and* a large vendor behind it
- there is a **Snowflake** relationship; Polaris is the open-source core of Snowflake's managed
  catalog, so the model transfers
- an existing [HMS](../../hms/README.md) needs migrating and `polaris-tools`' catalog migrator is
  the path
- fine-grained catalog RBAC is a design requirement rather than a wish

## When not to use it

- it has to be **deployed by GitOps without hand-holding** — see the note below; this is where it
  loses
- a smaller runtime is wanted; Lakekeeper is a Rust binary against PostgreSQL, Polaris is a JVM
  service
- **an administrative UI matters to the team** — the console exists and is not the reason to
  choose this
- metadata federation beyond Iceberg is the goal — [Gravitino](../gravitino/README.md)

## Notes

Recorded from evaluating it here:

> Does not support Helm OCI.
>
> It has a UI/console, but it is so bad that there is no Helm repository — let alone OCI.

The original note is blunter than that. The verdict stands as written and it is worth taking
literally rather than softening: **the packaging is the problem, and the console does not
compensate for it.**

**On the chart.** [`helm/helmrepository.yaml`](helm/helmrepository.yaml) points Flux at
`https://downloads.apache.org/polaris/helm-chart`, and [`helm/helmrelease.yaml`](helm/helmrelease.yaml)
pins chart 1.6.0 with empty `values`. That URL is the Apache distribution mirror — a directory of
release artefacts — rather than a maintained chart repository with an index that is expected to
stay available. Apache mirrors rotate content: older releases move to `archive.apache.org`, which
means a pinned version can stop resolving without anything in this repository changing. For a
component in the query path, a chart source that can disappear underneath a GitOps controller is a
real operational risk, not a stylistic objection.

And there is no OCI publication at all. Compare [Gravitino](../gravitino/README.md), which
publishes its chart to Docker Hub as an OCI artefact — immature, but at least reachable through
the same registry and credentials as the images.

**On the console.** Polaris ships a web UI for administering catalogs, principals and grants. The
recorded assessment is that it is bad, and the argument made alongside it is the interesting part:
a project that has not managed to publish a Helm repository is not a project whose UI is likely to
have received serious attention either. Packaging and interface polish tend to be produced by the
same kind of effort — the work of making something usable by people who did not build it.

Take the practical conclusion rather than the insult: **do not choose Polaris for its UI.**
Administer it through its API, and expect the console to be a viewer.

**What is genuinely good here** is the specification compliance and the migration tooling. Polaris
implements the REST spec thoroughly and `polaris-tools` gives a supported way off HMS. If the
chart situation resolves — an official OCI publication, on a repository that is not a distribution
mirror — this becomes a serious candidate. The recommendation in
[`../README.md`](../README.md#7-how-this-applies-to-pikakube) points at
[Lakekeeper](../lakekeeper/README.md) instead, for deployability rather than for protocol
differences. There are none worth mentioning: that is what a specification is for.

---

[← Iceberg REST catalogs](../README.md)
