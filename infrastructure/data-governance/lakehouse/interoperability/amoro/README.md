[← Interoperability](../README.md)

# Apache Amoro

<https://github.com/apache/amoro>

---

## The problem it solves

Not really interoperability, despite where it is filed. **Amoro is a management service for
lakehouse tables** — it runs the maintenance that table formats require and that almost nobody
schedules.

[`table-formats/`](../../table-formats/README.md#5-the-part-everyone-forgets-maintenance) states
the problem plainly: the features are adopted, the operations are not. Four jobs have to run
forever, and if they do not, the platform degrades quietly:

| Job | Without it |
|---|---|
| **Compaction** | thousands of small files; query planning takes longer than the scan |
| **Snapshot expiry** | history grows forever, and storage cost with it |
| **Orphan file cleanup** | files from failed writes are never referenced and never deleted |
| Manifest rewriting | the metadata itself becomes slow to read |

[Iceberg](../../table-formats/iceberg/README.md) exposes these as procedures —
`rewrite_data_files`, `expire_snapshots`, `remove_orphan_files` — but exposing them is not running
them. Amoro's central idea, its **self-optimizing** service, is to run them continuously and
automatically rather than as a set of cron jobs each team writes again.

It also puts a management layer on top: a catalog view of the tables under its care, per-table
optimisation state, and resource groups for the optimiser workers.

That is a genuinely useful thing to have. **The small-files problem is what actually degrades
lakehouse platforms**, and it arrives gradually enough that nobody notices until queries are slow.

## When to use it

- there are many Iceberg or [Paimon](../../table-formats/paimon/README.md) tables and **no
  maintenance is scheduled** for any of them
- writing and operating per-table compaction jobs is not a good use of the team's time
- a single view of which tables are optimised and which are not is worth having
- the engine versions in play are older ones — see the notes; this is the one place its
  conservatism is an advantage

## When not to use it

- a small number of tables — scheduled `rewrite_data_files` and `expire_snapshots` from
  [Airflow](../../../../data-engineering/orchestration/airflow/README.md) is less machinery for
  the same result
- the catalog already offers maintenance as a service — some do; check before adding a component
- current versions of Iceberg, [Spark](../../../../data-engineering/processing/spark/README.md),
  [Flink](../../../../data-streaming/processing/flink/README.md) or Trino are required — see the
  notes
- **the project's activity level is a blocker**, which for a maintenance service it reasonably
  might be

## Notes

Recorded from evaluating it:

> Compatible with old versions of Spark, Flink and Trino. Nice, but half dead.

- [apache/amoro#3876](https://github.com/apache/amoro/issues/3876)
- [the `iceberg.version` line in `pom.xml`](https://github.com/apache/amoro/blob/master/pom.xml#L106)

Both halves of that note matter, and they pull in opposite directions.

**The compatibility half is a real feature.** Supporting older Spark, Flink and Trino releases is
useful in an estate that cannot upgrade its engines on someone else's schedule — which is most
estates. Tools that only support the latest versions are frequently unusable for exactly that
reason.

**The "half dead" half is the problem**, and the two links are the evidence for it. The `pom.xml`
line is the pinned `iceberg.version` the project builds against: it is what the compatibility claim
is made of, and it is also the ceiling. A pinned Iceberg version that lags means new format
features and fixes are not available through Amoro, and the gap widens with every Iceberg release
rather than staying constant.

**Why this is worse here than it would be elsewhere.** A stalling project is always a risk. A
stalling project that would sit in the maintenance path of every table is a different category:

| | The risk |
|---|---|
| It stops keeping up with Iceberg | tables written by current engines may not be optimisable |
| It stops being maintained | the component that rewrites your data files is unmaintained |
| It has to be removed later | every table it manages needs a maintenance path again — and now urgently |

The last row is the practical one. Maintenance is not a feature you can drop for a quarter; if
Amoro is what compacts the tables and it has to be removed, the replacement is needed the same
week.

**The alternative is not exotic.** Iceberg's maintenance procedures are callable SQL, and running
them on a schedule from [Airflow](../../../../data-engineering/orchestration/airflow/README.md) is
a job, not a platform. That is more code than adopting Amoro and considerably less risk — and it
is the recommendation for a platform of this size.

The Helm deployment is mapped here for evaluation. Nothing about it should be read as a decision
to run it.

Related: [`metadata-catalog/`](../../../metadata-catalog/README.md), because some catalogs now
offer table maintenance as a service — which would make this component unnecessary rather than
merely risky.

---

[← Interoperability](../README.md)
