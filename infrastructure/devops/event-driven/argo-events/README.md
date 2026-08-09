[← Event-driven](../README.md)

# Argo Events

<https://github.com/argoproj/argo-events>
<https://github.com/argoproj/argo-helm>

Upstream examples: <https://github.com/argoproj/argo-events/tree/master/examples>

---

## The problem it solves

Something happened somewhere — a webhook fired, a file landed in S3, a message arrived on Kafka, a
calendar time passed, a Kubernetes resource changed — and something should happen in the cluster as
a result.

The usual answer is a small service that listens and calls the Kubernetes API. Then a second one.
Then a third, each with its own retry logic, its own authentication, its own idea of what to do
when it restarts mid-event, and no shared way to see what fired and what did not.

Argo Events makes that a declarative, three-part pipeline:

| Resource | Role |
|---|---|
| **EventSource** | listens to the outside world and publishes onto the bus — webhooks, S3, Kafka, SQS, calendar, Redis, GitHub, GitLab, resource changes, and many more |
| **EventBus** | the transport between the two halves — NATS JetStream by default, Kafka as an alternative |
| **Sensor** | subscribes to events, evaluates **dependencies**, and fires **triggers** |

The Sensor is where the value is. It can wait on **multiple dependencies** and combine them with
boolean logic, so "when both the upload finished and the approval webhook fired" is a declared
condition rather than a state machine somebody wrote. It can filter events by their contents, and it
can extract fields from the payload and inject them into whatever it creates.

Triggers cover Argo Workflows, arbitrary Kubernetes resources, HTTP requests, AWS Lambda, Kafka,
NATS, Slack, and custom triggers.

## When to use it

- **Argo Workflows is in use** and workflows need to start from external events rather than a
  schedule. This is the pairing the project was built for and where it is strongest
- several event sources need to be handled uniformly, with one place to look at what arrived
- an action must wait on **more than one** event, or on events matching a content filter
- payload data from the event has to parameterise what gets created — the `parameters` block maps
  a field from the event onto a field in the triggered resource

## When not to use it

- **for scaling.** Argo Events triggers actions; it does not adjust replica counts. Reacting to
  queue depth is [KEDA](../keda/README.md), and the two are regularly confused
- for a single webhook that starts a single job. An `EventSource`, an `EventBus`, a `Sensor`, and
  the NATS cluster underneath is a lot of infrastructure for one endpoint
- for reacting to **Kubernetes** events with a small script — that is
  [shell-operator](../shell-operator/README.md), which needs no bus and no CRDs beyond its own
  configuration
- if nobody will operate the EventBus. It is a stateful component, and when it is unhealthy events
  are lost silently, which is the worst failure mode this category has

## Notes

Three recorded references. The project, <https://github.com/argoproj/argo-events>; the chart
repository, <https://github.com/argoproj/argo-helm>, which is shared across the whole Argo family
rather than per-project; and the upstream examples directory,
<https://github.com/argoproj/argo-events/tree/master/examples>, which is the most useful part of the
project's documentation and worth reading before writing anything.

**One recorded command**, for reaching the webhook EventSource from a laptop:

```
kubectl -n argo-events port-forward $(kubectl -n argo-events get pod -l eventsource-name=webhook -o name) 12000:12000 &
```

The detail worth extracting: the EventSource's Pod is selected by the label
`eventsource-name=<name>`, not by the resource name, and the port is whatever the EventSource
declares. With the port-forward running, a `POST` to `localhost:12000/example` drives the whole
pipeline end to end.

**Deployed here**, via a Flux `HelmRelease` from the Argo Helm repository, with a complete worked
example under `example/`:

| File | What it establishes |
|---|---|
| `eventbus.yaml` | the transport the other two halves talk over |
| `eventsource.yaml` | a webhook server on port `12000`, endpoint `/example`, `POST` only |
| `sensor.yaml` | depends on that event and triggers an Argo `Workflow`, mapping the request **body** into the workflow's `message` parameter |
| `rbac-sensor.yaml` | the permissions the Sensor needs to create resources |
| `rbac-workflow.yaml` | the permissions the created Workflow runs with |

Two RBAC files for one example is not accidental, and it is the part most people get wrong on the
first attempt: the Sensor's ServiceAccount needs permission to **create** the Workflow, and the
Workflow's own ServiceAccount needs permission to do whatever the Workflow does. They are separate
identities with separate blast radii, and conflating them hands every triggered workflow the
Sensor's rights.

The parameter mapping in the Sensor is the other thing to study — `src.dataKey: body` into
`dest: spec.arguments.parameters.0.value` is how an external payload becomes an input to work
running in the cluster, and it is the whole point of the tool.

---

[← Event-driven](../README.md)
