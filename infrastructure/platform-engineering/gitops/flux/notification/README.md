[← Flux](../README.md)

# Flux notifications

Reconciliation that fails silently is reconciliation you cannot trust.

---

## The problem it solves

Flux corrects drift on a timer and says nothing. A `HelmRelease` that has been failing to upgrade for
a week presents exactly like one that is fine — the cluster is still running the old release, no pod
crashed, and no alert fired. The failure is recorded in the object's status conditions, where nobody
is looking.

notification-controller closes that. It watches events emitted by the other controllers and forwards
them outward, and it does it through three objects:

| Object | Role |
|---|---|
| `Provider` | where events go — Slack, Telegram, Teams, a generic webhook, Alertmanager |
| `Alert` | which events go there — filtered by source kind, name and severity |
| `Receiver` | the other direction: an inbound webhook that triggers reconciliation |

The `Receiver` half is worth knowing about even if unused here. It is what makes push-on-commit
possible without abandoning the pull model: a Git webhook hits the receiver, which tells
source-controller to fetch now instead of at the next interval. The cluster still pulls; it is simply
told when.

## When to use it

- always, for **failure** events — this is the only signal that a reconciliation loop has stopped
  converging
- when the team's incident channel should learn about a failed `HelmRelease` from the platform rather
  than from a user
- when commit-to-reconcile latency matters and waiting out the interval is too slow (`Receiver`)
- when Flux events should reach Alertmanager and be handled by the same routing as everything else

## When not to use it

- events at `info` severity forwarded to a chat channel — every successful reconciliation on every
  interval becomes a message, the channel is muted within a day, and the failures are muted with it
- as a substitute for metrics; this reports discrete events, not trends. Reconciliation duration and
  failure rate belong on a dashboard
- when nobody owns the destination channel — an alert with no owner is noise with a delivery
  mechanism

## Notes

There was no original note for this folder. What follows is read from the three manifests, which are
a complete and working example of the pattern — with two decisions in it that should not be copied
as-is.

### What is configured

A **Telegram** `Provider` in `flux-system`, pointing at `https://api.telegram.org`, delivering to
channel `@fluxcd`, with its bot token in a `secretRef` named `telegram-token`.

An `Alert` bound to that provider with:

```yaml
  summary: "Cluster addons impacted in us-east-2"
  eventSeverity: info
  eventSources:
    - kind: Kustomization
      name: '*'
```

### Three things to fix before this is useful

- **It is not installed.** notification-controller is **commented out** of the `components` list in
  the `FluxInstance` — see [`flux-operator/`](../flux-operator/README.md). These objects would be
  accepted only once the CRDs exist, and nothing acts on them today. The alerting is written and
  inert, which is the single most consequential gap in
  [`gitops/`](../../README.md): the reconciliation loop this platform depends on has no failure
  signal at all.
- **`eventSeverity: info` forwards everything.** Every successful reconciliation of every
  `Kustomization`, on every interval, becomes a Telegram message. The setting that makes this
  survivable is `error`. Start there, and add `info` for a narrow set of sources only if someone
  actually wants the running commentary.
- **The `summary` is inherited from an example.** "Cluster addons impacted in us-east-2" describes an
  AWS region this platform does not run in — the `FluxInstance` targets an Azure-flavoured node pool.
  The summary is prepended to every message, so this is the text that would arrive during a real
  incident, pointing at the wrong place.

### The token

`secret.yaml` carries `stringData.token` with a placeholder — the base64 of a string of `x`s, which
is a placeholder written twice over rather than a leaked credential. Note the field is `stringData`,
so Kubernetes encodes it; supplying an already-base64 value there produces a double-encoded token
that the provider will reject with an unhelpful error.

A real bot token must not be committed. The two options are the ones used elsewhere in this
repository: a secrets controller that materialises the `Secret` from an external store, or the token
supplied out-of-band and only its name referenced here.

### Choosing a provider

Telegram is a reasonable choice for a personal platform and an unusual one for a team. The property
that matters for a failure signal is whether the destination is **somewhere an on-call person is
already looking**. For most organisations that is Slack, Teams, or — better — Alertmanager, so that
Flux failures route through the same silencing, grouping and escalation as every other alert instead
of forming a parallel notification path nobody maintains.

---

[← Flux](../README.md)
