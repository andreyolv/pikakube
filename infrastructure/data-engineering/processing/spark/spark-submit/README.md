[← Spark](../README.md)

# spark-submit

Submitting directly, without an operator.

Tools covered: [`spark-on-k8s`](spark-on-k8s/README.md)

---

## What it is

The native way to launch a Spark application: `spark-submit` talks to the Kubernetes API
server, creates a driver pod, and the driver creates its executors.

```bash
spark-submit \
  --master k8s://https://<api-server> \
  --deploy-mode cluster \
  --conf spark.kubernetes.container.image=<image> \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  local:///opt/app/job.py
```

No operator, no CRD — Spark talks to Kubernetes itself.

## When this is the right shape

- **one-off** or ad-hoc submissions
- interactive work from a notebook, in client mode
- an [orchestrator](../../../orchestration/README.md) already owns scheduling, retries and dependencies, and only needs to launch something
- you would rather not run an operator

## When it is not

- **recurring** jobs — they should be Kubernetes objects, reconciled from Git. See [`kubernetes-operator/`](../kubernetes-operator/README.md)
- you want status, events and restart policy handled by a controller
- many jobs need consistent configuration; a template in an operator beats a shell script repeated

## What has to be set up either way

Easy to miss when submitting directly, because nothing prompts for it:

| Requirement | Why |
|---|---|
| **ServiceAccount and RBAC** | the driver creates executor pods, and needs permission to |
| Container image | with the application and its dependencies |
| `deploy-mode cluster` | in client mode the driver dies with the submitting process |
| Event log configuration | or the finished job leaves nothing — see [history server](../spark-history-server/README.md) |

## The tool here

| Tool | What it adds | Detail |
|---|---|---|
| **spark-on-k8s** | a Python client and CLI wrapping submission, plus a UI for watching apps | [→](spark-on-k8s/README.md) |

It sits between raw `spark-submit` and a full operator: programmatic submission from Python,
which fits an orchestrator calling it directly rather than shelling out.

---

[← Spark](../README.md)
