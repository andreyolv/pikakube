[← Event-driven](../README.md)

# KEDA

<https://github.com/kedacore/keda>
<https://github.com/kedacore/charts>

Sub-components: [`keda-http/`](keda-http/README.md) ·
[`keda-custom-external-scaler/`](keda-custom-external-scaler/README.md)

Recorded issues (OCI chart support):
<https://github.com/kedacore/charts/issues/20> ·
<https://github.com/kedacore/charts/issues/363>

---

## The problem it solves

The Horizontal Pod Autoscaler scales on CPU and memory. Almost nothing that actually needs scaling
correlates with CPU and memory.

A consumer draining a RabbitMQ queue is not CPU-bound — it is blocked on I/O, sitting at 8% CPU
while a hundred thousand messages pile up behind it. A Kafka consumer group falling behind shows the
same picture. A batch job that only needs to exist between 08:00 and 18:00 has no CPU signal at all
when it should be scaled to zero, because it is not running. In every one of these cases the correct
scaling signal lives **outside the cluster**, in the system producing the work.

KEDA supplies that signal, and adds the one thing the HPA cannot do at all.

### The two things it does

**1. Scale on external metrics.** KEDA registers as a Kubernetes *external metrics adapter*, so an
HPA can scale on queue depth, consumer lag, a Prometheus query, a SQL result, object-storage
object counts, cloud queue lengths, and around seventy other sources. You declare a `ScaledObject`;
KEDA creates and manages the underlying HPA.

**2. Scale to and from zero.** This is the part the HPA genuinely cannot do — `minReplicas: 0` is
not a valid HPA configuration, because with zero Pods there is no metric to read. KEDA solves it by
handling the 0→1 transition itself: it polls the trigger directly, and when the source becomes
*active* it scales the workload to one and hands control to the HPA from there. Scaling back to
zero is KEDA's job again.

That distinction is encoded in the trigger fields:

| Field | Meaning |
|---|---|
| `value` | the target the HPA scales towards once running |
| `activationValue` | the threshold that takes the workload from **0 to 1** |
| `pollingInterval` | how often KEDA asks the source |
| `cooldownPeriod` | how long the source must stay inactive before scaling back to zero |

### Why scale-to-zero is the interesting half

The cost model of a Kubernetes platform is dominated by workloads that exist without doing
anything. A dozen dev-environment consumers, a nightly batch worker, an internal tool used twice a
week — each holds requests against the scheduler around the clock so that nodes are provisioned for
capacity that is idle most of the time. Scaling those to zero returns real node capacity, and the
cluster autoscaler turns returned capacity into fewer machines. This is one of the highest-leverage
cost levers available on a Kubernetes platform and it requires no application changes — which is
the point of contact between this folder and the FinOps discipline.

### The two resources

| Resource | For | Behaviour |
|---|---|---|
| `ScaledObject` | Deployments, StatefulSets, custom resources with `/scale` | adjusts the replica count of a long-running workload |
| `ScaledJob` | `Job` | creates **a Job per unit of work** instead of scaling replicas |

`ScaledJob` is the right choice when each message is a discrete, long-running task that must not be
interrupted mid-flight — scaling a Deployment down can kill a consumer halfway through a job,
whereas a Job runs to completion.

Credentials for triggers go in a `TriggerAuthentication`, so connection strings and passwords are
referenced from Secrets rather than written into the `ScaledObject`.

## When to use it

- **any consumer of a queue, topic or stream.** Queue depth and consumer lag are the correct signal
  and CPU is not
- workloads that should not exist when there is no work — the cost argument above
- scheduled scaling with `cron`, which is a far better fit than a `CronJob` that patches a replica
  count
- scaling on a Prometheus query, which covers everything that already has a metric: request rate,
  latency, error budget, custom application counters
- **as the default event-driven scaling mechanism on this platform.** It is a CNCF graduated project,
  it is widely deployed, and it does not require applications to change

## When not to use it

- for straightforward CPU-bound web services. A plain HPA is fine and adds no components
- **for scaling HTTP services to zero** — KEDA core needs a metric that exists while the workload
  is at zero replicas, and "an HTTP request arrived" is not one. That needs a component in the
  request path: [`keda-http/`](keda-http/README.md), or [KubeElasti](../kubeelasti/README.md)
- for anything where a cold start is unacceptable. Scale-from-zero means the first unit of work
  waits for a Pod to be scheduled, an image to be present, and the process to become ready
- as a general event-routing mechanism. KEDA reads a source to decide **how many replicas**; it does
  not deliver events or trigger workflows — that is [argo-events](../argo-events/README.md)

## Notes

Four recorded references.

**The project and the charts**, in separate repositories: <https://github.com/kedacore/keda> and
<https://github.com/kedacore/charts>.

**The recorded finding: no OCI repository support.** The note reads *"not support oci repository"*,
with two issues attached:

| Issue | What it says |
|---|---|
| [charts#20](https://github.com/kedacore/charts/issues/20) | *"Publish Helm chart to an OCI-compatible repo to support versioning."* KEDA moved chart hosting from a CDN to GitHub Pages, losing versioning in the process; the issue asks for an OCI registry instead. **Open.** |
| [charts#363](https://github.com/kedacore/charts/issues/363) | *"Chart versions management."* Releasing charts became awkward after KEDA moved to hotfix release cycles; the proposals include moving charts to different storage or a dedicated release branch. **Open.** |

Why this is recorded at the top level of the folder rather than buried: in a Flux-based GitOps
setup the natural source type is an `OCIRepository`, and KEDA cannot be consumed that way. It has to
be a classic `HelmRepository` pointing at GitHub Pages. That is why the `HelmRelease` in this
repository uses `kind: HelmRepository` while newer tools here use `OCIRepository` — the
inconsistency is upstream's, not a mistake in the manifests. Both issues remain open.

**Deployed here**, under `keda/`, with a set of worked scaler examples that are more useful than the
upstream documentation because they record what was actually run:

| Scaler | What the example does |
|---|---|
| `cron` | `minReplicaCount: 0`, `maxReplicaCount: 1`, a `America/Sao_Paulo` timezone, and start/end expressions. The commented-out values (`0 8 * * 1-5` / `0 18 * * 1-5`) show the intended production shape: up on weekday mornings, down in the evening |
| `rabbitmq` | `mode: QueueLength`, `value: "5"`, `activationValue: "5"`, scaling `perf-test` from zero. The clearest demonstration of the 0→1 versus 1→N split |
| `postgresql` (`keda_airflow.yaml`) | scales the Airflow scheduler on a **SQL query** counting `running` and `queued` task instances — `SELECT ceil(COUNT(*)::decimal / 16) FROM task_instance WHERE state='running' OR state='queued'`. `minReplicaCount: 1`, so this one is about capacity rather than cost |
| `kafka`, `kafka-sasl`, `kafka-tls`, `prometheus`, `mongodb`, `postgres`, `kubernetes-workload` | placeholders — mapped, not yet configured |

The RabbitMQ example has a **plaintext password in the `host` field**. It works, and it is exactly
what `TriggerAuthentication` exists to prevent. Anything beyond a scratch cluster should reference a
Secret instead.

---

[← Event-driven](../README.md)
