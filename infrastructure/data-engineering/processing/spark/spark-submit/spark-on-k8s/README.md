[← spark-submit](../README.md)

# spark-on-k8s

<https://github.com/hussein-awala/spark-on-k8s>

---

## What it is

A Python client and CLI for submitting Spark applications to Kubernetes, plus a small web UI
for watching them.

It sits between raw [`spark-submit`](../README.md) and a full
[operator](../../kubernetes-operator/README.md):

| | `spark-submit` | **spark-on-k8s** | Operator |
|---|---|---|---|
| Interface | shell | **Python and CLI** | CRD |
| Job is a Kubernetes object | no | no | yes |
| GitOps | no | no | yes |
| Programmatic submission | shelling out | **native** | via the API |
| UI | none | included | third-party |

## When it is useful

- **an orchestrator submits from Python** — an Airflow task calling a library rather than shelling out to `spark-submit`
- a service needs to launch Spark jobs programmatically
- you want visibility into running applications without deploying an operator

## When not to use it

- recurring jobs that should live in Git as manifests — [operator](../../kubernetes-operator/README.md)
- a one-off submission, where plain `spark-submit` is fewer moving parts
- you already use an operator; this would be a second submission path

## The Airflow angle

Airflow's Spark operators generally shell out to `spark-submit`, which means parsing output to
find out what happened. A Python client gives structured status instead — which is the concrete
reason to prefer this in a DAG.

The alternative is submitting through the [Kubernetes operator](../../kubernetes-operator/README.md)
and having Airflow watch the CRD, which keeps the job as a Kubernetes object. That is the more
GitOps-consistent path when jobs are recurring.

---

[← spark-submit](../README.md)
