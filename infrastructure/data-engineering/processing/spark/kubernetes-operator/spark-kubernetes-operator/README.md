[← Kubernetes operator](../README.md)

# Apache Spark Kubernetes Operator

<https://github.com/apache/spark-kubernetes-operator>

---

## What it is

The **official** Spark operator, under the Apache Spark project itself — managing
`SparkApplication` and `SparkCluster` resources on Kubernetes.

It succeeds the widely-used `kubeflow/spark-operator` (formerly GoogleCloudPlatform's), which
was the de facto choice for years and lived outside the Spark project.

That lineage matters when choosing: the community one has more deployments and material behind
it; this one has the Spark project behind it and is where new development goes.

## When to use it

- recurring Spark jobs that should be Kubernetes objects — see [`../README.md`](../README.md)
- alignment with the Spark project rather than a third-party operator
- new deployments, where following upstream is worth more than the older ecosystem

## When not to use it

- an existing `kubeflow/spark-operator` deployment that works — migrating has a cost and little immediate return
- one-off submissions, where [`spark-submit`](../../spark-submit/README.md) is enough
- the orchestrator already owns job submission

## What to check before adopting

Being the official operator does not mean being the more mature one. Worth verifying for your
version:

- feature parity with `kubeflow/spark-operator` for what you actually use — scheduling, volumes, dynamic allocation, monitoring
- Spark version support
- whether the `SparkCluster` resource fits your model, or only `SparkApplication` matters

## Related

- Shuffle, which decides whether dynamic allocation works: [`shuffle/`](../../shuffle/README.md)
- Event logs, without which finished jobs are undiagnosable: [`spark-history-server/`](../../spark-history-server/README.md)

Both are configuration on the `SparkApplication`, and both are easier to set once in a template
than to retrofit across every job.

---

[← Kubernetes operator](../README.md)
