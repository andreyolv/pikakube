[← Serverless](../README.md)

# OpenWhisk

<https://github.com/apache/openwhisk>
<https://github.com/apache/openwhisk-deploy-kube>

---

## The problem it solves

Apache OpenWhisk is the **oldest** open-source serverless platform of the ones mapped here, and it
brings a genuinely different programming model — one built around events and composition rather
than around HTTP endpoints.

| Concept | What it is |
|---|---|
| **Action** | a function, in any supported language, or a container |
| **Trigger** | a named event stream |
| **Rule** | binds a trigger to an action — the association is a resource you create, not code |
| **Sequence** | actions chained, each one's output feeding the next, without an orchestrator |
| **Package** | a group of actions and feeds, with shared parameters |

The rule is the interesting piece. Elsewhere, "when X happens, run Y" is written inside the
function or inside a trigger CRD attached to it; in OpenWhisk it is a first-class object between
them, so one trigger can drive several actions and an action can be rebound without being changed.

Two repositories, as recorded: `apache/openwhisk` is the platform, `apache/openwhisk-deploy-kube`
is the Kubernetes deployment and the Helm chart.

## When to use it

- the **triggers/rules/sequences** model is genuinely what you want — it is the strongest reason to
  pick OpenWhisk over anything else here
- polyglot by default, with actions written in whichever language suits each one
- an Apache governance and licensing story matters to the organisation

## When not to use it

- **the cluster is small.** This is the practical blocker. The Kubernetes deployment is not one
  controller — it runs a controller, invokers, CouchDB for state, Kafka for the invocation queue,
  ZooKeeper, Redis and an nginx front end. That is a distributed system to operate before a single
  function runs
- you want scale-to-zero economics; the fixed footprint above never scales down
- the requirement is HTTP handlers with autoscaling — [OpenFaaS](../openfaas/README.md) or
  [Knative](../knative/README.md) do that with a fraction of the moving parts
- you are already running Kafka for [data streaming](../../../data-streaming/README.md) and would
  now be running a **second** Kafka, dedicated to the function platform, that nothing else can use

## Notes

**What is deployed here:** chart `openwhisk` 1.0.1 from `https://openwhisk.apache.org/charts`, in
the `openwhisk` namespace, with an empty `values` block — so the full default stack, including its
bundled datastores, would come up as-is.

The original note records nothing beyond the two repository links, which is itself the finding:
this one was catalogued rather than tried. Given the footprint described above, that is a
reasonable place to have stopped — the cost of evaluating OpenWhisk properly is materially higher
than the cost of evaluating any of its neighbours in this folder.

If it is ever revisited, the thing to check first is whether the bundled CouchDB and Kafka can be
pointed at existing instances rather than deployed alongside. That single question decides whether
this is a component or a platform of its own.

---

[← Serverless](../README.md)
