[← Governance platforms](../README.md)

# OpenMetadata

<https://github.com/open-metadata/OpenMetadata>
<https://github.com/open-metadata/openmetadata-helm-charts>

---

## The problem it solves

The most coherent of the open-source governance platforms: catalogue, lineage, data quality,
glossary and classification designed **as one product** rather than assembled from parts.

That coherence is the practical difference. Quality test results appear beside the dataset they
describe, lineage connects to the same entities, and ownership is one field rather than three
systems' opinions.

| Capability | Detail |
|---|---|
| **Discovery** | search across datasets, with descriptions, tags and popularity |
| **Data quality** | tests defined and executed **inside** the platform, results shown on the dataset |
| Lineage | ingested from connectors and from [OpenLineage](../../lineage/open-lineage/README.md) |
| **Glossary** | business terms mapped to physical columns |
| Classification | PII tagging, with automatic detection |
| Profiling | distributions, null rates, cardinality over time |
| Ownership | teams and users attached to every entity |
| Connectors | a wide catalogue, with scheduled ingestion |

**The built-in quality feature is the differentiator.** Elsewhere, quality lives in
[Soda](../../quality/soda/README.md) or [Great Expectations](../../quality/great-expectations/README.md)
and the catalogue links to it at best. Here a test is defined against a table in the catalogue and
its history is shown on that table's page — which is what makes "can I trust this?" answerable in
the place people are already looking.

## When to use it

- a governance platform is genuinely wanted, and **metadata is already being produced**
- quality and catalogue should be one thing rather than two integrated things
- the glossary and classification features will actually be used
- an open-source platform that **installs** matters — see the notes

## When not to use it

- **nothing is producing metadata automatically yet** — see
  [`../README.md`](../README.md#2-the-trap); this is the precondition, not a detail
- discovery and lineage are the whole requirement —
  [OpenDataDiscovery](../opendatadiscovery/README.md) is much less to run
- the widest possible connector catalogue is the deciding factor —
  [DataHub](../datahub/README.md) has more
- OCI-packaged Helm charts are a hard requirement — see the notes

## Notes

Recorded from actually deploying it:

```bash
k port-forward svc/openmetadata 8585
k port-forward svc/openmetadata-dependencies-web 8080
```

Credentials found during setup: `admin` / `admin` on the dependencies UI, and
`admin@open-metadata.org` / `admin` for OpenMetadata itself. **Those are defaults and must be
changed** — they are documented publicly, which makes them credentials in name only.

Three issues recorded, and each means something different:

| Issue | What it means |
|---|---|
| [openmetadata-helm-charts#236](https://github.com/open-metadata/openmetadata-helm-charts/issues/236) | a deployment problem encountered during install |
| [**#344**](https://github.com/open-metadata/openmetadata-helm-charts/issues/344) and [PR #478](https://github.com/open-metadata/openmetadata-helm-charts/pull/478) | **no OCI Helm support** |
| [OpenMetadata#29597](https://github.com/open-metadata/OpenMetadata/issues/29597) | `/api/v1/system/config/auth` serves a frozen/stale response |

**The OCI point matters in this repository specifically.** Everything here is deployed as a Flux
`HelmRelease`, and the direction of travel is `OCIRepository` rather than `HelmRepository` — see
the migration in [`platform-engineering/gitops/`](../../../platform-engineering/gitops/README.md). A chart
without OCI packaging means keeping a `HelmRepository` source for this one component, which works
and is inconsistent with the rest.

The **stale auth config** bug is worth knowing before configuring SSO: the endpoint that tells the
frontend how to authenticate can serve a cached response, so an authentication change appears not
to take effect. That is a confusing failure to debug without knowing it exists.

## The verdict for this platform

**This is the one to pursue**, and the reason is comparative rather than absolute: it installs,
and [DataHub](../datahub/README.md) did not — the recorded finding there is that its chart *"never
works"*, and a Spark lineage run produced nothing visible in the UI.

For a large distributed application, whether it deploys is most of the evaluation.

The precondition still applies and is why nothing is deployed yet: **this platform is not
producing metadata automatically.** Switching on [OpenLineage](../../lineage/README.md) in
Airflow, Spark and dbt is the step that makes a catalogue worth having, and doing it in the other
order is the failure described in [`../README.md`](../README.md#2-the-trap).

---

[← Governance platforms](../README.md)
