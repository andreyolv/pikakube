[← Data catalogs](../README.md)

# Amundsen

<https://github.com/amundsen-io/amundsen>

---

## What it was

Lyft's data discovery platform, and for several years the reference open-source answer to *"what
tables do we have and who owns them?"*

The design was influential: a search-first interface over table metadata, with popularity ranking
derived from actual query logs — so the tables people use most surface first. That idea has been
adopted widely since.

| Component | Role |
|---|---|
| Frontend | the search and browse interface |
| Metadata service | backed by Neo4j or Atlas |
| Search service | Elasticsearch |
| Databuilder | the ingestion framework |

## The state of the project

Stated first, because it decides everything else.

**The project is dead.** Development has effectively stopped, the maintainers have moved on, and
the community has migrated to [OpenMetadata](../../platform/open-metadata/README.md) and
[DataHub](../../platform/datahub/README.md).

That is not a marginal judgement. For a component that would sit at the centre of a governance
programme, adopting a project with no active development means no fixes, no security updates, and
no answers when something breaks.

## Notes

Recorded from evaluating it here:

> Dead project.
>
> The Helm chart is broken —
> [amundsen-io/amundsen#2219](https://github.com/amundsen-io/amundsen/issues/2219)

Both findings matter, and the second is the more informative one.

A broken Helm chart with an open issue and no fix is the clearest available signal about a
project's health — more reliable than a star count, a landing page, or a last-commit date that
reflects a dependency bump. It means nobody deploying it recently found it worth fixing.

This is also a good illustration of why
[`data-governance/`](../../README.md) records deployment findings rather than feature lists. Every
tool in this discipline claims to solve data discovery; the difference between them is whether
they install, and that is only discoverable by trying.

## What to use instead

| Requirement | Tool |
|---|---|
| A governance platform | [OpenMetadata](../../platform/open-metadata/README.md) — the most complete, and it installs |
| The widest connector catalogue | [DataHub](../../platform/datahub/README.md) — with its own recorded problems |
| Discovery and lineage, lightly | [OpenDataDiscovery](../../platform/opendatadiscovery/README.md) |

And the prior question from [`../../README.md`](../../README.md#5-the-order-that-works): a
catalogue is a **view over metadata that already exists**. If nothing is producing metadata
automatically, deploying any of these produces an empty product with a search box.

## Why it is still in the catalogue

Mapping a solution space includes recording what is **dead**, for the same reason
[RethinkDB](../../../databases/nosql/document/rethinkdb/README.md) and
[OrientDB](../../../databases/nosql/multi-model/orientdb/README.md) are kept in
[`databases/`](../../../databases/README.md).

Without that, someone evaluating data catalogues finds Amundsen in a search result, reads a
feature list from 2021, and spends a week discovering what one line here could have told them.

---

[← Data catalogs](../README.md)
