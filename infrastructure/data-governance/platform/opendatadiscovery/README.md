[← Governance platforms](../README.md)

# OpenDataDiscovery

<https://github.com/opendatadiscovery/odd-platform>
<https://github.com/opendatadiscovery/charts>
<https://opendatadiscovery.org/>

---

## What it is

The **light** option in this folder: discovery and lineage, without the glossary, classification,
access-request and quality-management surface that
[OpenMetadata](../open-metadata/README.md) and [DataHub](../datahub/README.md) bring.

That is a deliberate position rather than an incomplete one. Its premise is that most teams
adopting a governance platform actually want two things — *what data exists* and *where it came
from* — and pay for six.

| Capability | Detail |
|---|---|
| **Discovery** | search across datasets, with owners and descriptions |
| **Lineage** | dataset and job level, ingested from adapters |
| **ODD Specification** | an open metadata spec, so producers push rather than being crawled |
| Adapters | for common warehouses, orchestrators and BI tools |
| Data quality | test results surfaced, ingested from external tools |
| Ownership | teams and owners per entity |
| Alerting | on schema changes and quality failures |

## The specification is the interesting part

Like [OpenLineage](../../lineage/open-lineage/README.md), OpenDataDiscovery publishes an **open
specification** — the ODD Spec — and a set of adapters that speak it.

That matters for the same reason: metadata is **pushed** in a documented format rather than being
crawled by connectors that belong to one vendor. A source that speaks ODD works with anything that
consumes ODD, and writing an adapter for an in-house system is a defined task rather than a
plugin against someone's internal model.

Whether it gains adoption outside the project is the open question. OpenLineage succeeded because
Airflow, Spark and dbt implemented it; ODD has a smaller adoption footprint so far.

## When to use it

- **discovery and lineage are the whole requirement**, and the rest would go unused
- a smaller footprint matters — less to deploy, less to populate, less to abandon
- the push model suits the estate better than connector-based crawling
- a first governance deployment, where proving value beats covering every feature

## When not to use it

- quality and catalogue should be one product —
  [OpenMetadata](../open-metadata/README.md)
- the widest connector catalogue is the deciding factor —
  [DataHub](../datahub/README.md)
- glossary, classification and access workflows are genuinely needed
- **nothing is producing metadata automatically yet** — the precondition in
  [`../README.md`](../README.md#2-the-trap) applies to every option here

## The argument for starting small

Worth making, because it cuts against the instinct to pick the most capable platform.

The failure described in [`../README.md`](../README.md#2-the-trap) — deploy, populate by hand once,
go stale, get abandoned — is more likely with a larger product, because there is more to populate
and more of it stays empty. An empty glossary and an unused classification taxonomy make a
catalogue look neglected, which is how people stop opening it.

A platform that does two things and does them from automatic sources is more likely to survive
than one that does eight and does six of them badly.

That is the case for OpenDataDiscovery, and it is a legitimate one even though the other two are
more capable.

## Notes

Mapped with the [official charts](https://github.com/opendatadiscovery/charts).

Nothing here is deployed. The recommendation in
[`../README.md`](../README.md#7-how-this-applies-to-pikakube) is
[OpenMetadata](../open-metadata/README.md), on the practical grounds that it installs where
DataHub did not.

OpenDataDiscovery is the option to reconsider if that judgement changes — specifically if
OpenMetadata's surface turns out to be more than this platform will populate. The sequence in
[`../../README.md`](../../README.md#5-the-order-that-works) applies either way: quality checks,
then automatic lineage, then a catalogue over what those produce.

---

[← Governance platforms](../README.md)
