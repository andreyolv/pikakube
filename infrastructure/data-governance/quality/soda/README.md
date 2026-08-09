[← Data quality](../README.md)

# Soda

<https://github.com/sodadata/soda-core>

Working examples: [`postgres/`](postgres/) · [`pyspark/`](pyspark/)

---

## The problem it solves

Data quality checks written as **YAML**, executed against a real source, failing when the data is
wrong.

```yaml
checks for orders:
  - row_count > 0
  - missing_count(customer_id) = 0
  - duplicate_count(order_id) = 0
  - freshness(created_at) < 24h
  - invalid_percent(status) = 0:
      valid values: [pending, shipped, cancelled]
```

The YAML is the argument. A check written like that can be **read, and often written, by an
analyst** — and the knowledge of what "correct" means for a table generally lives with analysts
rather than with the platform team.

That is the property that separates it from
[Great Expectations](../great-expectations/README.md) and
[Pandera](../pandera/README.md), where checks are Python.

## When to use it

- checks should be readable by people who do not write Python
- the data is in a **warehouse or a database**, queried with SQL
- checks run as a pipeline step, failing the run
- the same engine is wanted for [contracts](../../contract/README.md) later

## When not to use it

- Spark at scale, where [Deequ](../deequ/README.md) computes metrics in a single pass
- validating **DataFrames in code** — [Pandera](../pandera/README.md) is closer to the data
- profiling and data docs are the requirement —
  [Great Expectations](../great-expectations/README.md)
- unit-testing transformations — [chispa](../chispa/README.md) is the tool for that

## Running it

```bash
pip install soda-core
pip install soda-core-postgres

soda test-connection -c configuration.yml -d my_postgres
soda scan -c configuration.yml -d my_postgres checks.yml -V
```

Three files, and the separation is deliberate:

| File | Contains |
|---|---|
| `configuration.yml` | how to connect — host, credentials, and it should read from the environment |
| `checks.yml` | what to verify |
| The invocation | which data source, which checks |

Keeping credentials out of `configuration.yml` matters on Kubernetes: the file belongs in Git, and
the values belong in a Secret referenced through environment variables.

`soda scan` returns a **non-zero exit code** when checks fail, which is what makes it usable as a
pipeline step rather than a report.

## Orchestrating from Airflow

The realistic shape for this platform, and the reason the
orchestration references below are kept.

A scan is a task in the DAG that produces the data, placed **before** the publish step:

| Position | Effect |
|---|---|
| After transform, before publish | bad data never becomes visible; the DAG fails |
| After publish | consumers have already read it |
| A separate scheduled DAG | drift detection, not prevention |

The first is the default worth taking — see
[`../README.md`](../README.md#3-where-the-check-runs).

Because the scan exits non-zero, a failing check fails the task, which fails the DAG, which
reaches whatever alerting the platform already has. That is the connection the quality folder
names as the gap: a check is only a control when its failure goes somewhere.

References recorded here:
[Soda's orchestration guide](https://docs.soda.io/soda-library/orchestrate-scans.html),
[a walkthrough with Airflow](https://ahmed-mokbel.medium.com/how-to-use-soda-for-data-quality-checks-with-apache-airflow-cf249a737b5a),
and an [Airflow Summit talk](https://airflowsummit.org/slides/2023/2-York-1400-East-Sleep-Test-Repeat.pdf).

## Notes

The [`postgres/`](postgres/) example is complete — connection configuration, the check file, and
the commands — along with
[Soda's own example](https://github.com/sodadata/soda-core/blob/main/examples/postgres_example.md),
a [workshop check set](https://github.com/sodadata/datatalks-workshop/tree/main/checks) and a
[video walkthrough](https://www.youtube.com/watch?v=CSqHZ1eJ5is).

That combination — a working Postgres example plus an Airflow orchestration pattern — is the most
practically complete quality setup in this repository, and it is the recommended starting point in
[`../README.md`](../README.md#8-how-this-applies-to-pikakube).

One thing to keep separate: **the contracts module is a different story.**
[`contract/soda/`](../../contract/soda/README.md) records that its documentation is broken and the
documented import path does not exist. That finding applies to contracts only — the check engine
described on this page works.

---

[← Data quality](../README.md)
