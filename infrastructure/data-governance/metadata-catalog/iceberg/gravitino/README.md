[← Iceberg REST catalogs](../README.md)

# Apache Gravitino

<https://github.com/apache/gravitino>

---

## The problem it solves

Gravitino is the odd entry in this folder: it is not primarily an Iceberg REST catalog. It is a
**metadata lake** — a single service that federates metadata across several kinds of source, and
exposes an Iceberg REST endpoint as one of its interfaces.

Originally Datastrato's, now an Apache project.

| Property | Detail |
|---|---|
| Scope | **multiple sources** — Hive, Iceberg, JDBC databases, message systems, filesets |
| Model | metalake → catalog → schema → table, one namespace over everything |
| Interfaces | its own REST API, **an Iceberg REST catalog endpoint**, and a Hive-compatible one |
| State | a relational database |
| Language | Java |
| Extras | tag and access-control layers on top of the federated metadata |

The pitch is a single logical namespace over sources that would otherwise each need their own
catalog — query a Hive table and a PostgreSQL table without the engine holding two sets of catalog
configuration. That is a broader problem than "where is the current Iceberg snapshot", and it is
both the reason to look at Gravitino and the reason not to adopt it *only* as an Iceberg catalog.

## When to use it

- the requirement is genuinely **federation**: Hive, Iceberg, JDBC and Kafka metadata under one
  namespace
- there is an existing [HMS](../../hms/README.md) estate that has to keep working while new
  Iceberg tables are created — Gravitino can front both
- a metadata layer that engines *and* a governance platform can read from is the target
  architecture
- the maturity note below is acceptable because this is exploratory

## When not to use it

- an **Iceberg REST catalog is all that is needed** — then the narrower implementations are the
  better fit: [Lakekeeper](../lakekeeper/README.md) or [Polaris](../polaris/README.md), which do
  one job and have more of it behind them
- this is the **query path** and the deployment has to be dependable now — see the note
- the federation would front sources nobody actually queries together, which is the usual outcome
  when a federating layer is adopted before the need exists
- a **data catalogue for people** is what is wanted — Gravitino is infrastructure; that is
  [`platform/`](../../../platform/README.md)

## Notes

Recorded from evaluating it here:

> The OCI Helm chart was recently created — very low maturity.

Both halves of that matter, and they pull in opposite directions.

**The OCI chart is, on paper, the best packaging in this folder.**
[`helm/ocirepository.yaml`](helm/ocirepository.yaml) points Flux at
`oci://registry-1.docker.io/apache/gravitino-helm` with tag 1.3.11 and an explicit
`layerSelector`, and [`helm/helmrelease.yaml`](helm/helmrelease.yaml) consumes it through a
`chartRef`. That is exactly the shape this repository's GitOps setup wants, and it is the thing
[Lakekeeper](../lakekeeper/README.md) and [Polaris](../polaris/README.md) both fail to provide.

**And it is new, which is the problem.** A chart published recently has not been through the cycle
that makes a chart trustworthy: upgrades between versions, values that turn out to be wrong,
resources that were missing, the first person who tried to run it with an external database. Being
OCI-packaged is a distribution property, not a quality one — the chart being fetchable in the
right format says nothing about whether `helm upgrade` works.

The `digest:` field in the OCIRepository is left empty. Pinning it is worth doing here
specifically: an immature chart on a mutable Docker Hub tag is two sources of drift stacked on top
of each other.

**Where that leaves it.** This is the honest tension in the folder, stated in
[`../README.md`](../README.md#7-how-this-applies-to-pikakube): the implementation with the
packaging this platform wants is the one with the least maturity behind it, and the implementation
with the best deployment story publishes over a plain Helm repository. Neither of those is a
protocol problem — the REST catalog is a specification and all three implement it.

The judgement recorded here is that low maturity outweighs convenient packaging **for a component
in the query path**. If the catalog is unavailable or upgrades badly, every engine stops being able
to resolve a table. That is a different risk class from a chart that has to be fetched over HTTPS
instead of OCI.

Worth revisiting: Gravitino is an active Apache project and this note is about a chart that was
new when it was written. The federation story is also the most interesting one in this folder if
the platform ever needs a single namespace over
[Hive](../../hms/README.md), Iceberg and the
[JDBC sources](../../../../databases/README.md) at once.

---

[← Iceberg REST catalogs](../README.md)
