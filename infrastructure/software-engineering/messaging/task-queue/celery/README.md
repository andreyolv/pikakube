[← Task queue](../README.md)

# Celery

<https://github.com/celery/celery>
<https://github.com/mher/flower>

---

## The problem it solves

Running Python functions somewhere else, later, reliably — with everything that implies already
built.

`send_email.delay(user_id)` returns immediately; a worker process elsewhere runs the function. The
value is not the deferral, which is easy. It is everything around it:

| Capability | What it saves you writing |
|---|---|
| **Retries** | per task, with exponential backoff, jitter and a maximum count |
| **Routing** | tasks to named queues, and worker pools bound to specific queues |
| **Beat** | a scheduler that submits periodic tasks into the queue |
| **Canvas** | chains, groups and chords — workflows built from tasks |
| Time limits | soft (raises an exception) and hard (kills the worker child) |
| Rate limits | per task, to protect a downstream that cannot take the load |
| Result backend | optional storage of return values |
| Worker pools | prefork, threads, gevent, eventlet — chosen per workload shape |

Two details decide most deployments. The **pool type**: prefork is the default and right for
CPU-bound work, while gevent or threads suit IO-bound tasks where a process per task wastes
memory. And **`acks_late`**: by default Celery acknowledges a task *before* running it, so a
worker crash loses it silently; `acks_late=True` acknowledges after completion, which is what most
people assume is happening and is not.

**Celery is not a broker.** It needs [RabbitMQ](../../broker/rabbitmq/README.md) or
[Redis](../../../../databases/nosql/key-value/redis/README.md) underneath, and that choice — not
Celery's own configuration — decides whether a task can be lost. See
[`task-queue/`](../README.md#2-it-needs-a-broker-underneath).

## When to use it

- Python, and background work with **real requirements**: retries, routing, scheduling, chaining
- several classes of work that must not starve each other — separate queues, separate worker pools
- periodic tasks that belong in the same system as the on-demand ones, via Beat
- scale where a worker pool is genuinely sized and tuned, not just present
- an existing Celery estate — it is the default in Python and the ecosystem knows it

## When not to use it

- **the requirement is "run this function later" and nothing more** — RQ is a fraction of the
  configuration surface, see [`task-queue/`](../README.md#4-the-tools)
- the requirement is scheduling, not distribution — APScheduler, or a Kubernetes `CronJob`
- work with dependencies between steps, lineage and backfills — that is an orchestrator,
  [`orchestration/`](../../../../data-engineering/orchestration/README.md)
- other services in other languages must consume the work — use a
  [broker](../../broker/README.md) directly; Celery's message format is its own
- jobs measured in hours — that is a batch job, and a `Job` resource is the right shape

## Notes

Recorded during evaluation:

> **helm chart muito novo** — *the Helm chart is very new*

That is the whole finding, and it matters more than it sounds.

**Celery is normally deployed as part of the application, not as a platform service.** A worker is
your application image started with `celery -A app worker` — it imports your task code, carries
your dependencies and your settings, and must be versioned and deployed with the application, or
a worker running old code will pick up a task the new code just sent. That makes it a
`Deployment` in the application's own manifests, not an installation in an infrastructure
repository.

A Helm chart for Celery is therefore a recent, and slightly unusual, way of doing it. Consequences
to expect:

| Expect | Because |
|---|---|
| The chart deploys **workers, not your tasks** | the task code still has to come from your image |
| Values and CRD-free interfaces will change | a new chart has not settled its interface yet |
| Little material when something breaks | the community answer is still a hand-written `Deployment` |
| The broker is **not** included | it is a separate dependency, chosen and run separately |

### As installed here

There is no chart repository, and the `HelmRelease` shows it: the source is a Flux
**`GitRepository`** cloning `https://github.com/celery/celery.git` at tag **`v5.5.0rc4`**, with an
`ignore` block excluding everything except `/helm-chart`, and the release installs the chart named
`helm-chart` from that clone into the `celery` namespace.

Reading that back: the chart is **inside the Celery repository**, not published anywhere, and the
pinned tag is a **release candidate**. Both are the recorded note in concrete form. It works, and
it is worth being explicit about what it is — pinning to a tag rather than a branch is the right
call here, because a chart at this stage can change shape between commits.

The values comment points at the upstream reference:
<https://github.com/celery/celery/blob/main/helm-chart/values.yaml>

### Flower

<https://github.com/mher/flower> — the monitoring UI for Celery, recorded alongside it.

It connects to the broker and shows what the CLI cannot: tasks in flight and completed with their
arguments and runtimes, worker pools with their concurrency and status, queue lengths, and the
ability to revoke a task, terminate it or restart a pool. It also exposes Prometheus metrics, which
is the part that turns it from a debugging tool into something
[Prometheus](../../../../observability/metrics/storage/prometheus/README.md) can alert on.

The honest limits:

- it is **not a durable record** — by default its history lives in memory and disappears with the pod
- it can revoke and terminate tasks, so it is a control interface; do not expose it without
  authentication in front of it
- it does not replace alerting. A human looking at Flower is a human who already knows something
  is wrong

Without Flower, or something like it, a Celery deployment has exactly the failure mode
[`task-queue/`](../README.md#5-long-running-tasks-and-visibility) describes: long-running tasks in
workers nobody watches, on queues nobody has graphed.

---

[← Task queue](../README.md)
