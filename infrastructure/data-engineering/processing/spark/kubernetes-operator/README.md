[← Spark](../README.md)

# Kubernetes operator

Tools covered: [`spark-kubernetes-operator`](spark-kubernetes-operator/README.md)

---

## The problem it solves

`spark-submit` launches a job and exits. Nothing tracks it, nothing retries it, and the job is
not a Kubernetes object — so it cannot be described, watched, or managed by Flux.

An operator makes a Spark job a **CRD**:

```yaml
apiVersion: spark.apache.org/v1
kind: SparkApplication
metadata:
  name: daily-aggregation
spec:
  # image, main class, resources, dependencies
```

What that changes:

| With the operator | Without |
|---|---|
| `kubectl get sparkapplications` | look for driver pods and guess |
| Status and events on the object | parse driver logs |
| Retries and restart policy declared | scripted, per job |
| **Reconciled from Git** | submitted by whatever ran the script |
| Scheduled applications as objects | a CronJob wrapping `spark-submit` |

The GitOps property is the real one. A recurring job becomes a manifest in the repository like
everything else in this platform.

## When to use it

- **recurring** Spark jobs, which is most of them
- GitOps — jobs belong in the repository, not in a submission script
- you want status, events and retries handled by a controller

## When not to use it

- one-off or interactive submissions — [`spark-submit/`](../spark-submit/README.md)
- the orchestrator already owns submission and tracking; see below

## Operator or orchestrator

Both can submit and track Spark jobs, and the distinction matters:

| | Operator | [Airflow](../../../orchestration/airflow/README.md) |
|---|---|---|
| Job definition | a Kubernetes object | a DAG task |
| Scheduling | its own, or a CronJob | the orchestrator's |
| Dependencies between jobs | none | the whole point |
| Backfill | no | yes |

If the job stands alone, the operator is sufficient and simpler. If it is one step among many
with dependencies and backfill, the orchestrator should own it — submitting through the
operator or directly.

Using both without deciding produces two places that think they own the job.

---

[← Spark](../README.md)
