[← Falco](../README.md)

# falco-exporter

<https://github.com/falcosecurity/falco-exporter>
<https://github.com/falcosecurity/charts>

Subscribes to Falco's gRPC event stream and exposes Prometheus metrics. Turns a stream of individual
detections into something you can graph, alert on, and reason about over time.

---

## The problem it solves

Falco produces events. An event is a single fact: at 03:14 a shell was spawned in container X. That
is the right shape for an investigation and the wrong shape for almost everything else.

Questions you cannot answer from a stream of events without aggregating them:

| Question | Why it matters |
|---|---|
| Is the alert rate going up or down? | the only honest measure of whether tuning is working |
| Which rules produce most of the volume? | the top ten rules are almost always the tuning backlog |
| Is Falco still running on every node? | a dead agent produces silence, which looks exactly like a quiet cluster |
| Is Falco **dropping** events? | a saturated agent is a blind agent, and nothing else tells you |

falco-exporter answers all four. It connects to Falco over gRPC, counts events by rule, priority,
namespace, pod and node, and serves them at `/metrics` for Prometheus.

The metrics fall into two useful groups:

- **`falco_events_total`** and friends — counters by rule and priority. The material for dashboards
  and for rate-of-change alerts.
- **Drop metrics** — how many syscalls Falco could not keep up with. This is the one people miss.
  Falco degrades by dropping, not by crashing, so a node under load quietly stops seeing things and
  reports no error. If you take one metric from this exporter, take this one.

The chart also ships a Grafana dashboard, enabled here, so there is something to look at without
building panels first.

## When to use it

- **Prometheus is already the monitoring stack.** Then this is nearly free and the Falco data joins
  everything else you already alert on.
- **During tuning.** "Which rule is producing 80% of the alerts" is a Prometheus query with this
  exporter and a manual log-grep without it. Tuning is a ranking problem, and this produces the
  ranking.
- **To alert on absence.** The most valuable Falco alert is not a detection — it is
  `up{job="falco-exporter"} == 0`, or a node whose event count went to zero. Security agents fail
  silently, and silence is the failure signal.
- **To watch for drops.** On a data platform where Spark and Airflow generate syscalls at high rate,
  the agent hitting its throughput limit is a realistic scenario and an invisible one.
- **To show progress.** A downward trend in alert volume over a quarter is the evidence that the
  tuning work was worth funding.

## When not to use it

- **As the alerting path for detections.** A metric counter tells you *that* something fired, not
  *what* happened — no process name, no file path, no command line. Alerting on a counter and then
  having no event detail to investigate is a bad position. Route the events themselves through
  falcosidekick and use metrics for rates and health.
- **Instead of storing events.** Aggregation destroys the detail an investigation needs. This is a
  complement to an event sink, not a replacement.
- **Where cardinality is a concern.** Labelling by pod and namespace on a large, churning cluster
  produces a lot of series. Worth checking against the Prometheus budget before enabling everything.
- **Without Falco's gRPC output enabled.** It has nothing to subscribe to otherwise, and the failure
  is a connection error rather than an obvious misconfiguration.

Worth knowing about the project's status: falco-exporter has been superseded upstream by metrics
support built into Falco and falcosidekick, which expose Prometheus metrics natively. The chart still
works, and the version deployed here (0.9.7) is stable, but a new deployment should check whether the
native path covers the requirement before adding a separate component.

## Notes

There was no `doc.md` for this folder. What follows is the state of the deployment and how it relates
to the rest.

### How it is deployed here

`helm/helmrelease.yaml`, chart `falco-exporter` 0.9.7 in the `falco` namespace:

| Setting | Meaning |
|---|---|
| `dependsOn: falco` (namespace `falco`) | Flux waits for Falco; the exporter is useless without it |
| `grafanaDashboard.enabled: true` | the dashboard is created as a ConfigMap |
| `grafanaDashboard.namespace: falco` | the ConfigMap is created in the `falco` namespace |

That last setting is the one to verify rather than assume. Grafana's sidecar discovers dashboards by
**label** across namespaces (or within a configured set of namespaces), so a dashboard ConfigMap in
`falco` is only picked up if Grafana's dashboard sidecar is watching all namespaces, or `falco`
specifically. If the dashboard does not appear, this is why, and the fix is on the Grafana side, not
here.

### The dependency on Falco's gRPC settings

This exporter works only because `helm/helmrelease.yaml` in [`../`](../README.md) sets both
`falco.grpc.enabled` and `falco.grpc_output.enabled`. Those two settings are what
[falco-talon](../falco-talon/README.md) depends on as well.

If either is turned off during a values cleanup, both companions stop receiving anything — and
neither logs a loud failure. The connection between those settings and these two components is worth
knowing before editing the Falco values.

### Where it fits

The Falco folder has three companions and they cover three different needs:

| Companion | Answers |
|---|---|
| [`event-generator/`](../event-generator/README.md) | is it working at all? |
| **`falco-exporter/`** | how much is it seeing, and is it keeping up? |
| [`falco-talon/`](../falco-talon/README.md) | what happens when something fires? |

This is the one that makes the tuning loop in [`../../README.md`](../../README.md#tuning-is-the-job)
tractable — sorting alerts by frequency is the whole method, and it needs the alerts counted.

No Prometheus alert rules are defined anywhere in this folder, so the metrics currently exist and
nothing watches them. The two rules worth writing first are "Falco is not running on a node" and
"Falco is dropping events".

---

[← Falco](../README.md)
