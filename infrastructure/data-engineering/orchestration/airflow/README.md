[← Orchestration](../README.md)

# Apache Airflow

<https://github.com/apache/airflow>
<https://github.com/apache/airflow-client-python>
<https://airflow.apache.org/docs/>

---

## The problem it solves

The default orchestrator: DAGs as Python, a scheduler that respects dependencies, retries with
backoff, backfill, and the largest operator ecosystem of anything in this folder.

Its dominance is ecosystem rather than design. Whatever the task is — submit a Spark job, run
dbt, call an API, move a file between clouds — an operator exists, and someone has hit the
problem you are about to hit.

## When to use it

- **the default**, unless there is a specific reason otherwise
- the platform orchestrates more than data — ML, infrastructure jobs, maintenance
- the ecosystem matters: operators, providers, and people who already know it

## When not to use it

- **assets** rather than tasks are the mental model — [Dagster](../dagster/README.md) makes lineage native
- pipelines should be declarative configuration — [Kestra](../kestra/README.md)
- a small footprint is required; Airflow is a scheduler, a webserver, a database and workers

## The KubernetesExecutor

The right shape on Kubernetes: each task becomes a pod, with its own resources, isolated from
the scheduler and from every other task. It is what prevents one memory-hungry task from taking
down the scheduling layer.

Two consequences worth knowing before adopting it:

**Service mesh sidecars break it.** A sidecar keeps running after the task container exits, so
the pod never completes and the task hangs forever. Batch workloads need explicit exclusion —
see [Linkerd](../../../network/service-mesh/linkerd/README.md).

**`pod_override` is how you customise per task**, and its behaviour has been a long-running
source of confusion — see the issues below.

## The ecosystem

| Project | What it adds |
|---|---|
| [astronomer-cosmos](https://github.com/astronomer/astronomer-cosmos) | runs dbt projects as native Airflow task groups, with per-model visibility instead of one opaque `dbt run` |
| [astro-sdk](https://github.com/astronomer/astro-sdk) | higher-level, dataframe-style API over operators |
| [dag-factory](https://github.com/astronomer/dag-factory) | DAGs generated from YAML |
| [airflow-dag-action](https://github.com/jayamanikharyono/airflow-dag-action) | CI validation for DAGs |
| [airflow-client-python](https://github.com/apache/airflow-client-python) | the REST API client |
| [agents](https://github.com/astronomer/agents) | Astronomer's agent work |

**Cosmos is the one worth singling out.** A single `dbt run` task tells you nothing about which
model failed; Cosmos turns each model into a task, which makes retries and failures meaningful.

---

## Notes

### Housekeeping

```bash
airflow db clean --clean-before-timestamp '2026-02-02' --dry-run --skip-archive --verbose
```

The metadata database grows without bound and eventually becomes the performance problem.
Run with `--dry-run` first, always.

### Does not support OCI repositories

<https://github.com/apache/airflow/issues/67837>

Which makes it the exception in a GitOps setup where everything else is an `OCIRepository`.

### General issues and discussions

- <https://github.com/apache/airflow/discussions/37336>
- <https://github.com/apache/airflow/discussions/37763>
- <https://github.com/apache/airflow/issues/39757>
- <https://github.com/apache/airflow/issues/18714>
- <https://github.com/apache/airflow/issues/9342>
- <https://github.com/apache/airflow/issues/37621>
- <https://github.com/apache/airflow/issues/29897>
- <https://github.com/apache/airflow/issues/20772>

### `pod_override`

- <https://github.com/apache/airflow/issues/22298>
- <https://github.com/apache/airflow/issues/10290>
- <https://github.com/apache/airflow/discussions/31990>
- <https://github.com/apache/airflow/issues/31988>
- <https://github.com/apache/airflow/pull/34505>

### Airflow 3 migration

<https://github.com/apache/airflow/issues/41641>

### Scheduler race condition

- <https://github.com/apache/airflow/issues/57470>
- <https://github.com/apache/airflow/issues/59349>

### `ti_finish` metrics disappearing

- <https://github.com/apache/airflow/issues/46805>
- <https://github.com/apache/airflow/issues/41822>
- <https://github.com/apache/airflow/issues/47992>
- <https://github.com/apache/airflow/issues/60276>

Relevant to anything alerting on task completion — see
[`observability/`](../../../observability/README.md).

### Custom UI

- <https://github.com/apache/airflow/pull/58411>
- <https://github.com/apache/airflow/issues/52251>

### Cosmos

<https://github.com/astronomer/astronomer-cosmos/issues/2029>

---

[← Orchestration](../README.md)
