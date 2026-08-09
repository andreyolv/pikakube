[← Stream processing](../README.md)

# Apache StreamPark

<https://github.com/apache/incubator-streampark>
<https://streampark.apache.org/>

---

## The problem it solves

Not processing — **managing the processing**. Running one Flink job is manageable; running forty
is where the pain is:

| Problem | Without a platform |
|---|---|
| Submission | a script per job, differing subtly |
| Versioning | which JAR is running, and which one was running last week |
| **Savepoints** | remembering to take one before stopping, and finding it again |
| Configuration | scattered across submission commands |
| Monitoring | per job, assembled |
| Access | everyone has cluster credentials |

StreamPark is a management layer over Flink and Spark jobs: a catalogue, versioned deployments,
savepoint handling, and a UI for people who should not be running `flink run`.

## When to use it

- **many** Flink or Spark jobs, operated by more than one person
- savepoint lifecycle is currently manual, which is where stateful upgrades go wrong
- non-platform teams need to deploy and monitor their own jobs
- job history and rollback matter

## When not to use it

- one or two jobs, where the [Flink operator](../flink/README.md) is enough
- jobs should be **Kubernetes objects** in Git — the operator plus GitOps covers that, and this adds a UI-managed layer beside it
- the project's incubating status is a concern for something this central

## The tension with GitOps

Worth naming. StreamPark manages jobs through its own interface and database. A GitOps
repository manages them as manifests.

Running both means two sources of truth for what is deployed — the same problem as any UI that
mutates cluster state. See [konga](../../../network/api-gateway/kong/konga/README.md) for the
same conclusion in a different domain.

The reconciliation is to decide which one owns deployment. If the answer is Git, the
[Flink operator](https://github.com/apache/flink-kubernetes-operator) plus Flux covers most of
what this offers, minus the UI.

---

## Notes

```bash
kubectl port-forward svc/streampark-service 10000
```

Default credentials: `admin` / `streampark`

Change them before exposing it — this can submit jobs to the cluster.

---

[← Stream processing](../README.md)
