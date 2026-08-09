[← Data quality](../README.md)

# Great Expectations

<https://github.com/great-expectations/great_expectations>

---

## What it is

The most complete data-quality framework in Python: a large library of expectations, automatic
profiling, and **data docs** — a generated HTML site showing what was validated and what passed.

```python
validator.expect_column_values_to_not_be_null("customer_id")
validator.expect_column_values_to_be_between("amount", min_value=0)
validator.expect_column_values_to_be_in_set("status", ["pending", "shipped"])
```

| Capability | Detail |
|---|---|
| **Expectation library** | hundreds, covering most things anyone checks |
| **Profiling** | point it at a dataset and it proposes expectations from what it sees |
| **Data docs** | a generated site — results, history, and what each expectation means |
| Checkpoints | named validation runs, wired into pipelines |
| Multi-backend | pandas, Spark, and SQL sources |
| Custom expectations | write your own when the library falls short |

**Profiling is the feature that gets people started.** Pointing it at an existing table and having
it propose expectations turns "we should add quality checks" from a blank page into a review
exercise, which is a much easier first step.

## When to use it

- **profiling** an unfamiliar dataset to discover what its constraints actually are
- data docs are wanted — a readable artefact showing what is validated
- the checks are complex enough to need real code
- Python is the pipeline language, across pandas, Spark and SQL

## When not to use it

- checks should be readable by analysts — [Soda](../soda/README.md)'s YAML is the better shape
- **the configuration surface is the obstacle** — see below
- Spark at scale, where [Deequ](../deequ/README.md)'s single-pass metrics matter
- schema validation close to a DataFrame — [Pandera](../pandera/README.md) is far less setup

## The adoption problem

Worth stating plainly, because it is the most common outcome.

Great Expectations is the most capable tool here and it has the most configuration: data contexts,
datasources, batch requests, expectation suites, checkpoints, and stores. Each concept is
reasonable; together they are enough that **adoption frequently stalls before the first check
runs.**

The API has also changed substantially between major versions, so a large share of the tutorials
and Stack Overflow answers describe a shape the installed version does not have. That is the same
class of problem recorded for [InfluxDB](../../../databases/nosql/timeseries/influxdb/README.md),
and it costs the same kind of time.

If the requirement is *"check that this table is not empty and this column is never null"*, the
distance between that sentence and a working Great Expectations setup is larger than the distance
to a working [Soda](../soda/README.md) setup.

## Notes

Recorded from evaluating it:

> Does not support Azure AD token-based authentication for Azure storage accounts —
> [great-expectations/great_expectations#6519](https://github.com/great-expectations/great_expectations/issues/6519)

That is a specific and consequential gap. It means connecting to Azure Blob Storage requires an
account key or a SAS token rather than a managed identity — a long-lived secret where the platform
would otherwise use a federated, rotating credential.

For an organisation whose security position is "no long-lived storage keys", that alone rules it
out for Azure-backed data, regardless of the tool's other merits. It is the kind of finding that
does not appear in a feature comparison and decides adoption.

Reference material kept here:
[an ETL pipeline example](https://github.com/hnawaz007/pythondataanalysis/blob/main/ETL%20Pipeline/GreatExpectations/Great%20Expectations%20Data%20Quality%20Tests.ipynb),
a [quick tutorial](https://github.com/prodramp/publiccode/blob/master/python/greatexpectation-work/05-Quick%20Great%20Expectations%20Tutorial.ipynb),
and a [PySpark DataFrame example](https://github.com/prodramp/publiccode/blob/master/python/greatexpectation-work/07-PySpark-DataFrame-with-GE.ipynb).

For this platform the recommendation remains [Soda](../soda/README.md) — see
[`../README.md`](../README.md#8-how-this-applies-to-pikakube) — because the working example, the
Airflow pattern and the YAML readability all point the same way.

Where Great Expectations still earns its place is **profiling**: pointing it at an unfamiliar
dataset to find out what its constraints actually are, then writing the resulting checks wherever
they are going to live.

---

[← Data quality](../README.md)
