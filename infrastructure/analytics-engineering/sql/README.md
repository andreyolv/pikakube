[← Analytics Engineering](../README.md)

# SQL

The language underneath everything else in this discipline.

---

## Why it has a folder

Every other folder here is a tool choice. This one is not — it is the thing that does not
change when the tools do.

Ingestion lands raw data, [transform](../transform/README.md) models it, the
[semantic layer](../semantic/README.md) defines metrics over it,
[BI tools](../viz/README.md) query it and [notebooks](../notebook/README.md) explore it. All of
it is SQL, executed by a warehouse or a
[query engine](../../data-engineering/query-engine/README.md).

That durability is the point: dbt may be replaced, Metabase may be replaced, the warehouse may
be replaced. The SQL knowledge transfers to all of it.

## Order of execution, which explains most confusion

SQL is written in one order and evaluated in another. Almost every "why doesn't this work"
question traces back to it:

```
FROM / JOIN  →  WHERE  →  GROUP BY  →  HAVING  →  SELECT  →  DISTINCT  →  ORDER BY  →  LIMIT
```

Consequences that follow directly:

| Symptom | Cause |
|---|---|
| An alias from `SELECT` cannot be used in `WHERE` | `SELECT` runs after `WHERE` |
| An alias **can** be used in `ORDER BY` | `ORDER BY` runs after `SELECT` |
| Filtering an aggregate needs `HAVING`, not `WHERE` | `WHERE` runs before the aggregation exists |
| `LEFT JOIN` plus a condition in `WHERE` behaves like an inner join | the filter runs after the join and discards the null rows |

The last one is the most expensive in practice: the join preserved the rows, and then the
filter silently threw them away. The fix is putting the condition in the `ON` clause.

## What actually matters for analytics work

| Topic | Why |
|---|---|
| **Window functions** | ranking, running totals, deduplication, period-over-period — most analytical questions are a window function |
| **CTEs** | readable, composable queries; the basis of how dbt models are written |
| **Join semantics** | inner, left, and the row-multiplication that a many-to-many join causes silently |
| **NULL behaviour** | `NULL != NULL`, and aggregates that skip nulls — a source of wrong numbers rather than errors |
| **Grouping sets, `ROLLUP`, `CUBE`** | multiple aggregation levels in one pass |
| `QUALIFY` | filtering on a window function directly, where the dialect supports it |

Deduplicating with `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)` and keeping row 1 is
probably the single most reused pattern in a data platform.

## Dialects

The standard is a starting point; every engine extends it. The differences that bite are date
handling, string functions, array and struct support, and window function extensions.

For a lakehouse this matters when moving between engines — a query written for Trino does not
necessarily run on Spark SQL. [SQLGlot](https://github.com/tobymao/sqlglot) is the usual answer
when transpilation is genuinely needed.

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| `SELECT *` in models | schema changes propagate silently downstream | explicit columns |
| Filtering a `LEFT JOIN` in `WHERE` | it becomes an inner join without saying so | put the condition in `ON` |
| Nested subqueries several levels deep | unreadable and unreviewable | CTEs |
| `DISTINCT` to fix duplicates | it hides a join that is multiplying rows | find the join |
| Business logic duplicated per query | the same metric, defined differently, twice | model it, or a [semantic layer](../semantic/README.md) |
| Assuming `NULL` comparisons behave | `NULL = NULL` is not true, and the row vanishes | `IS NULL`, or `COALESCE` deliberately |

---

[← Analytics Engineering](../README.md)
