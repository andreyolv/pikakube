[← Analytical databases](../README.md)

# Apache Kyuubi

<https://github.com/apache/kyuubi>

---

## The problem it solves

Not a database. **A multi-tenant SQL gateway** in front of engines that already exist — Spark
above all, and also Flink, Trino and Hive.

The problem it addresses is specific and familiar: Spark is a job-submission system, not a service
someone connects to. An analyst who wants to run SQL against the lakehouse needs a notebook, a
Spark session, cluster credentials and a way to size an application — none of which is what they
were trying to do.

Kyuubi puts a **JDBC/ODBC endpoint** in front, so any SQL client connects and gets a session:

| Capability | Detail |
|---|---|
| **JDBC / ODBC** | via the HiveServer2 protocol — BI tools and SQL clients connect unchanged |
| **Multi-tenancy** | sessions isolated per user, with their own engine instances |
| Engine lifecycle | Spark applications started, reused and stopped automatically |
| **Resource isolation** | one user's heavy query does not consume another's session |
| Authentication | Kerberos, LDAP, and pluggable options |
| Engine choice | Spark, Flink, Trino, Hive behind one endpoint |

## When to use it

- **Spark is the engine** and people need SQL access without submitting applications
- BI tools should connect to the lakehouse over JDBC
- several teams share a Spark cluster and need isolation between them
- Spark session management is currently done by hand, per user

## When not to use it

- **[Trino](../../../data-engineering/query-engine/README.md) is the query engine** — it already
  is a multi-tenant SQL service; Kyuubi in front of it adds a layer without adding the capability
- one team, using notebooks, where session management is not a problem
- interactive sub-second queries — Spark's startup and planning costs remain
- the analytical store is a database with its own SQL endpoint

## Kyuubi or Trino

The comparison that actually decides it, because they overlap in what the user sees:

| | Kyuubi | Trino |
|---|---|---|
| What it is | **a gateway** to engines | **a query engine** |
| Execution | Spark, Flink, Trino, Hive | its own MPP engine |
| Latency | Spark's | **lower** for interactive queries |
| Long-running ETL | **Spark's strength** | not its purpose |
| Federation across sources | via the engine | **native, many connectors** |
| Reuses existing Spark investment | **yes** | no |

**Trino if the requirement is interactive analytical SQL.** It is built for that and it is
faster at it.

**Kyuubi if Spark is already the platform** — the transformations, the UDFs, the libraries and the
tuning already exist there, and the requirement is to expose SQL access to it rather than to
introduce a second engine.

Running both is common and reasonable: Trino for interactive queries, Kyuubi for SQL access to the
Spark workloads.

## Notes

Mapped as the gateway option in this folder, and it is the entry that is not a database — which
is worth flagging, because it appears alongside [Databend](../databend/README.md) and
[ByConity](../byconity/README.md) and answers a different question entirely.

For this platform it is relevant because **Spark is genuinely deployed** — see
[`data-engineering/processing/spark/`](../../../data-engineering/processing/spark/README.md), with
the Kubernetes operator, history server and performance tooling all mapped.

That makes Kyuubi the natural way to give SQL access to it, rather than everyone submitting
applications or working through
[Jupyter](../../../analytics-engineering/notebook/jupyter/README.md). It connects directly to
[`analytics-engineering/viz/`](../../../analytics-engineering/viz/README.md), where Superset and
Metabase need a JDBC endpoint to point at.

The alternative worth weighing first is
[Trino](../../../data-engineering/query-engine/README.md), which is also mapped here and answers
the interactive case better.

---

[← Analytical databases](../README.md)
