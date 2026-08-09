[← Iceberg REST catalogs](../README.md)

# Lakekeeper

<https://github.com/lakekeeper/lakekeeper>

<https://github.com/lakekeeper/lakekeeper-charts>

<https://github.com/lakekeeper/lakekeeper-operator>

---

## The problem it solves

An **Iceberg REST catalog written in Rust**, backed by PostgreSQL — the same job as
[Polaris](../polaris/README.md), with a materially better deployment story.

The three repositories above are the reason it stands out in this folder. Most projects at this
stage ship a server and leave Kubernetes as an exercise; Lakekeeper publishes the server, a Helm
chart repository, **and** an operator. In a capability where every option has a packaging
complaint recorded against it, that is the distinguishing property.

| Property | Detail |
|---|---|
| Language | Rust — a single binary, small footprint, no JVM tuning |
| State | **PostgreSQL** |
| Protocol | the Iceberg REST catalog specification |
| Multi-tenancy | warehouses and projects as first-class objects |
| Authorisation | OpenFGA — relationship-based, table and namespace level |
| Identity | OIDC |
| **Credential vending** | supported — scoped, temporary storage access handed to engines |
| Packaging | Helm charts **and** an operator |

The authorisation model is the part worth noticing. Rather than bolting policy onto a metastore,
Lakekeeper treats *who may read this table* as catalog state, and combined with credential vending
that grant is what the engine's storage token is actually derived from. That is the full version
of what section 3 of [`../README.md`](../README.md#3-credential-vending) describes.

## When to use it

- an **Iceberg REST catalog is the requirement** and it has to be deployed on Kubernetes by
  something other than hand — this is the one with charts and an operator
- **table-level authorisation** matters, not just bucket policies
- **credential vending** is the goal: engines authenticate to the catalog and never hold S3 keys
- PostgreSQL is already operated well — with
  [CloudNativePG](../../../../databases/sql/postgresql/operator/cnpg/README.md) here, the
  dependency is a manifest rather than a new stateful system
- a JVM service is not wanted for a lookup path

## When not to use it

- the requirement is **metadata federation** across Hive, JDBC and Kafka as well as Iceberg —
  that is [Gravitino](../gravitino/README.md)
- an engine in the stack **cannot speak the REST catalog API** — then
  [HMS](../../hms/README.md) is still in the picture, and running both over the same tables is the
  anti-pattern rather than the workaround
- the GitOps setup **strictly requires OCI-packaged charts** — see the note below
- Apache-foundation governance is a procurement requirement; Lakekeeper is an independent project

## Notes

Recorded from evaluating it here:

> Test the Iceberg integration.
>
> Does not support OCI Helm.

**"Test the Iceberg integration"** is an open task, not a finding, and it is the honest state of
this deployment: the chart is wired up and the catalog has never had an engine pointed at it. The
[`helm/helmrelease.yaml`](helm/helmrelease.yaml) here configures the external database, disables
the bundled PostgreSQL subchart and switches on Prometheus scrape annotations — and configures **no
warehouse, no object-storage backend and no OIDC issuer.** Those are exactly the three things that
have to be right before Spark or Trino can create a table, and they are the part that has not been
attempted.

Concretely, "tested" would mean: register a warehouse against MinIO, create a namespace, have
[Spark](../../../../data-engineering/processing/spark/README.md) or
[Trino](../../../../data-engineering/query-engine/README.md) create and commit to an Iceberg
table through the REST endpoint, and confirm the engine received **vended credentials** rather
than using its own configured keys. Until that last part is verified, the catalog is doing the
easy half of the job.

**"Does not support OCI Helm"** is the packaging complaint, and it is the mildest of the three
recorded in this folder. Lakekeeper publishes its charts as a conventional Helm repository on
GitHub Pages — [`helm/helmrepository.yaml`](helm/helmrepository.yaml) points Flux at
`https://lakekeeper.github.io/lakekeeper-charts/` — rather than as OCI artefacts in a registry.

Why that matters at all: OCI charts are pulled from the same registry as the container images,
with the same authentication, the same mirroring and the same digest pinning. A GitHub Pages index
is an extra source type, an extra network dependency, and one that cannot be mirrored into a
private registry as easily. Flux supports both, so this is friction rather than a blocker —
compare [Polaris](../polaris/README.md), which has no usable Helm repository at all, and
[Gravitino](../gravitino/README.md), which ships OCI and very little maturity behind it.

**The PostgreSQL setup here is the good part.** [`postgres/cluster.yaml`](postgres/cluster.yaml)
declares a CloudNativePG cluster with pod monitoring enabled;
[`postgres/password.yaml`](postgres/password.yaml) and
[`postgres/externalsecret.yaml`](postgres/externalsecret.yaml) generate a 42-character password
and deliver it as a Secret with a `cnpg.io/reload` label, which the HelmRelease then consumes by
reference. No credential is written into a manifest. That is the pattern the
[HMS deployments](../../hms/hms-aws/README.md) in this repo do not follow, and it is worth
carrying across.

One thing to size correctly: the cluster is a **single instance with 2Gi of storage** and no
backup configured. Per section 6 of [`../README.md`](../README.md#6-anti-patterns), this database
holds the pointers without which the Parquet files in the bucket stop being tables.

---

[← Iceberg REST catalogs](../README.md)
