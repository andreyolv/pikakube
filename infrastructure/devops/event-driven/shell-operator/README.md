[← Event-driven](../README.md)

# shell-operator

<https://github.com/flant/shell-operator>

---

## The problem it solves

Writing a Kubernetes operator is a project. Client-go, informers, work queues, a reconcile loop,
leader election, CRDs, a build pipeline, a container image, and a Go codebase that somebody now
owns — all to run twenty lines of logic when a resource changes.

shell-operator collapses that to: **a script, plus a description of when to run it.**

You write hooks — shell, Python, anything executable. Each hook, when invoked with `--config`,
prints a JSON binding configuration describing what it wants to react to. shell-operator reads
that, sets up the watches, and executes the hook with the matching objects delivered as a JSON file
on disk.

| Binding | Fires on |
|---|---|
| `kubernetes` | create / update / delete of resources matching a kind, namespace, label or field selector |
| `schedule` | a cron expression |
| `onStartup` | operator startup, before anything else |

It handles the parts that are genuinely hard — informers, caching, filtering, deduplication, queue
ordering, retries — and leaves the logic to a script. The `jqFilter` option is the piece that makes
it practical at scale: it reduces watched objects to just the fields the hook cares about, so a hook
is only woken when something it actually looks at has changed.

It is also the foundation of Flant's addon-operator, which layers Helm releases on the same model.

## When to use it

- **glue automation**: label a namespace when it is created, write a ConfigMap when a Service
  appears, notify Slack when a specific resource changes, patch a resource that a chart got wrong
- one-off cluster policies too specific to be worth a policy engine, and too stateful to be a
  validating webhook
- prototyping a controller, to find out whether the reconcile logic is right before committing to
  building a real operator
- teams with no Go, where the alternative is a `CronJob` running `kubectl` in a loop — which is the
  same thing with worse semantics and no event delivery

## When not to use it

- **for anything that needs to be a real controller.** No status subresource handling, no finalizers
  worth the name, no structured conditions. If users will interact with the thing you are building,
  build an operator
- for policy enforcement — Kyverno and Gatekeeper (`security/2-cluster/policies/`) are the right
  tools and they act at admission time, whereas shell-operator reacts after the fact
- for scaling on events, which is [KEDA](../keda/README.md)
- for orchestrating multi-step, external-event-driven pipelines, which is
  [argo-events](../argo-events/README.md)
- where a shell script running with cluster-wide permissions is not acceptable. That is exactly what
  this is, and the RBAC is yours to scope

## Notes

The only recorded reference is the repository: <https://github.com/flant/shell-operator>.

**The recorded opinion: the documentation is bad.** The original note reads *"doc bosta"* — "the
docs are rubbish". Taken together with the same complaint recorded against
[KEDA's external scalers](../keda/keda-custom-external-scaler/README.md), it is a fair signal about
this whole corner of the ecosystem: the concepts are simple, and the written material assumes you
already know how they fit together.

The practical consequence is that the hook binding format — the JSON that a hook prints in response
to `--config` — is the thing to learn first, and it is best learned from the examples in the
repository rather than from prose. Everything else follows from it.

Nothing is deployed for this; it is mapped, not installed.

The reason it earns a place in this folder: it defines the **floor** of the event-driven category.
[Argo Events](../argo-events/README.md) is the heavy option with a bus and CRDs, KEDA is the
scaling-specific option, and shell-operator is the answer to "I just want to run this script when
that happens". Knowing that floor exists prevents deploying an event bus to solve a fifteen-line
problem.

---

[← Event-driven](../README.md)
