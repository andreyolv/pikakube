[← Data governance](../README.md)

# Data catalogs

What data exists, and what it means — and a folder that is mostly a graveyard.

Tools covered: [`unitycatalog`](unitycatalog/README.md) · [`magda`](magda/README.md) ·
[`amundsen`](amundsen/README.md) · [`atlas`](atlas/README.md)

Reference: <https://github.com/opendatadiscovery/awesome-data-catalogs>

---

## Read this folder for what it records

Two of the four entries here are **dead projects**, and that is the most useful thing this folder
contains.

| Tool | State |
|---|---|
| [Amundsen](amundsen/README.md) | **dead** — no active development, broken Helm chart |
| [Apache Atlas](atlas/README.md) | **dead** — project and chart both stalled, Hadoop-era dependencies |
| [Unity Catalog](unitycatalog/README.md) | active, and straddles two categories — see below |
| [Magda](magda/README.md) | active, and aimed at **open data portals** rather than platform metadata |

Both dead entries were, at different times, the obvious open-source answer to *"what tables do we
have?"* Anyone researching this today will find them near the top of search results with feature
lists that read well.

The maintained answers are in [`platform/`](../platform/README.md) —
OpenMetadata, DataHub, OpenDataDiscovery.

## The word "catalog" means two things

The distinction that runs through this whole discipline, restated because this folder is where it
causes the most confusion:

| | **This folder** — business catalog | [`metadata-catalog/`](../metadata-catalog/README.md) — technical catalog |
|---|---|---|
| Answers | what does this table mean, who owns it, can I trust it? | where are the files, and what is the current snapshot? |
| Consumed by | **people** | **query engines** |
| If it is down | discovery is inconvenient | **every query fails** |

**Unity Catalog is the confusing case**, and deliberately so: it aims to be both — a technical
catalog that Spark and Trino resolve tables through, *and* a governance layer with lineage and
access control. That ambition is why it sits here rather than in either folder cleanly.

## Magda is a different job again

Worth separating out, because adopting it for the wrong reason is easy.

Magda is built for **open data portals** — publishing datasets to an external audience, with
DCAT metadata, harvesting from other portals, and a public-facing search experience. Government
and research organisations are its users.

That is not the same problem as *"which of our internal tables should an analyst use?"* If the
requirement is a public data portal, Magda is a serious answer and nothing in
[`platform/`](../platform/README.md) is. If it is internal discovery, it is the wrong tool.

## What actually decides a catalogue's success

Not the tool. The sequence in
[`../README.md`](../README.md#5-the-order-that-works):

> A catalogue is a **view over metadata that already exists.** If nothing is producing metadata
> automatically, deploying a viewer produces an empty product with a search box.

The failure pattern is consistent enough to be predictable:

1. A catalogue is deployed, because it is the visible artefact
2. It is populated by hand, once
3. Nothing keeps it current
4. Six months later it is confidently wrong, and nobody opens it

That sequence has consumed a great many governance programmes, and it is why the recommended
order puts quality checks and automatic lineage first.

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Deploying a catalogue before metadata exists | an empty product; the discipline gets blamed | automatic collection first |
| Populating by hand | correct for a week | ingest from the systems that know |
| Adopting a dead project | no fixes, no updates, no answers | check commit activity before the feature list |
| Ownership left blank | the most valuable field, empty — questions still route by memory | make it mandatory |
| Confusing the two catalog meanings | expecting a discovery UI to serve Trino | see section 2 |
| An open-data portal used for internal metadata | a different problem, solved well | [`platform/`](../platform/README.md) |
| A glossary with no link to physical columns | a dictionary nobody consults | map terms to columns |

## How this applies to pikakube

Nothing here is deployed, and nothing here should be.

Two entries are dead, one is an open-data portal, and the fourth — Unity Catalog — is worth
tracking rather than adopting, for the packaging reasons on its page.

The maintained options are in [`platform/`](../platform/README.md), where the recorded findings
point at **OpenMetadata**: it installs, and [DataHub](../platform/datahub/README.md) did not.

The precondition still applies and is the reason none of it is deployed: this platform is not yet
producing metadata automatically. Switching on [OpenLineage](../lineage/README.md) in Airflow,
Spark and dbt is the step that makes a catalogue worth having — see
[`lineage/`](../lineage/README.md), where that is the named gap.

---

[← Data governance](../README.md)
