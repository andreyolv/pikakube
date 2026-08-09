[← Integration](../README.md)

# Dapr

<https://github.com/dapr/dapr>

---

## The problem it solves

Dapr — Distributed Application Runtime — moves the plumbing of a distributed system **out of your
code and into a sidecar**. The application talks HTTP or gRPC to `localhost`; the sidecar deals
with the actual broker, store, secret manager or service.

The unit is a **building block**, and each one is backed by a swappable *component*:

| Building block | What the application calls | What sits behind it |
|---|---|---|
| Service invocation | `localhost/v1.0/invoke/orders/method/...` | discovery, mTLS, retries, tracing |
| State management | get / set / delete against a key | Redis, PostgreSQL, Cassandra, and others |
| Publish and subscribe | publish to a topic name | Kafka, RabbitMQ, NATS, Redis Streams |
| Bindings | trigger on, or send to, an external system | queues, storage, SaaS APIs |
| Secrets | read a secret by name | Kubernetes secrets, Vault, cloud secret stores |
| Actors | a virtual actor with turn-based concurrency | the runtime places and activates them |

The payoff, when it lands: your service does not import a Kafka client, a Redis client and a
secrets SDK. It makes local HTTP calls, and the broker behind pub/sub is a YAML component you can
change without touching the code — in **any language**, because the interface is HTTP rather than
an SDK.

## When to use it

Dapr is worth its cost when several of these are true at once. One of them is not enough:

- **many services** — dozens, not five. The runtime is a fixed cost amortised across them
- **polyglot**. This is the strongest argument. Three languages means three Kafka clients, three
  retry implementations, three sets of bugs — or one HTTP contract
- **many backing stores**, and a genuine need to swap or standardise them: a real migration off a
  broker, or a requirement to run the same code against different infrastructure per environment
- portability across clouds or on-prem is an actual requirement with a date, not an aspiration
- the **actor model** fits the domain. This block has no easy equivalent, and where it fits it is
  the reason to adopt Dapr on its own

## When not to use it

- a handful of services, one language, one broker, one database. A shared library does all of this
  with no sidecar, no control plane and no extra hop
- **a service mesh is already running.** Service invocation, mTLS, retries and telemetry overlap
  almost completely with what the mesh already does — see
  [`network/service-mesh/`](../../../network/service-mesh/README.md). Running both means two
  sidecars per pod and two answers to "why was this retried"
- the sidecar cost is not acceptable: memory and CPU per replica, an extra hop on every call, and
  a readiness dependency your application did not previously have
- it is being adopted for a portability nobody will exercise. That is permanent complexity bought
  against a migration that will not happen

## Notes

**The recorded verdict: *"cool, but too much overengineering."***

That is the note as written, and it should be carried forward honestly rather than softened. It is
a judgement about fit, not a claim that the project is bad — the two halves of the sentence are
both meant. The building-block model *is* genuinely well designed, and it *is* far more machinery
than most platforms need.

The judgement is correct for this platform, and it is worth being explicit about why, because the
same reasoning is how to re-evaluate later:

| Condition where Dapr pays | Situation here |
|---|---|
| Dozens of services | not the case — the workloads mapped in this repository are platform components, not a service fleet |
| Polyglot fleet, all repeating the same client code | Python dominates; there is no duplicated client problem to solve |
| Several interchangeable backing stores | one broker at a time, chosen deliberately |
| Portability across clouds as a hard requirement | not present |

With none of those holding, what Dapr adds is a sidecar in every pod, a control plane, a set of
component CRDs and a new failure mode — to abstract dependencies that are not currently causing
pain. **The abstraction has to be cheaper than the problem it hides**, and here it is not.

Reasons that judgement might change: a genuine polyglot fleet, a broker migration that has to be
done without rewriting consumers, or a domain that wants virtual actors. Any of those flips it.

**What is deployed here:** chart `dapr` 1.14.1 from `https://dapr.github.io/helm-charts/`, in the
`dapr` namespace, with an empty `values` block.

**Dapr appears twice in this repository.** It is also an optional component of
[OpenFunction](../../serverless/openfunction/README.md), which uses it for the async function
runtime — and it is **disabled** there too. Two independent evaluations reaching the same
conclusion is a useful signal, and it is recorded here so the second one does not get made from
scratch.

---

[← Integration](../README.md)
