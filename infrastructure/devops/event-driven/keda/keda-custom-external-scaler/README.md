[← KEDA](../README.md)

# KEDA custom external scaler

<https://keda.sh/docs/2.15/concepts/external-scalers/>

Reference implementations:
<https://github.com/cloudnativedaysjp/dreamkast-external-scaler> ·
<https://github.com/rafaelcalleja/keda-upstream-deployment-scaler> ·
<https://github.com/maniSbindra/keda-error-threshold-and-queue-length-based-scaler>

---

## The problem it solves

KEDA ships around seventy built-in scalers. Occasionally the signal you need is not one of them: an
internal scheduling system, a licence server with a seat count, a bespoke queue, or a decision that
combines several inputs and cannot be expressed as one metric.

An **external scaler** is a gRPC service you write and run. KEDA calls it, and it answers. The
`ScaledObject` uses `type: external` and points at your service address; everything else about KEDA
— the HPA it manages, the 0→1 activation, the cooldown — works unchanged.

### The gRPC contract

| Method | Question it answers | Used for |
|---|---|---|
| `IsActive` | is there any work at all? | the **0 → 1** decision |
| `GetMetricSpec` | what metric name and target value? | configuring the HPA KEDA creates |
| `GetMetrics` | what is the current value? | the **1 → N** decision |
| `StreamIsActive` | *push* activity notifications instead of being polled | the "push" variant, for sources that can notify |

The split between `IsActive` and `GetMetrics` is the same split described in
[KEDA's README](../README.md): activation is KEDA's own job, and scaling beyond one replica is the
HPA's. An external scaler has to answer both questions, and answering only one is the most common
implementation mistake.

Implementing `StreamIsActive` turns the scaler into a *push* scaler — KEDA opens a long-lived stream
and reacts to notifications rather than polling on `pollingInterval`. It is more responsive and more
work to get right, particularly around reconnection.

## When to use it

- the scaling signal genuinely does not exist as a built-in scaler and cannot be reasonably exposed
  as a Prometheus metric
- the decision requires combining sources — for example error rate **and** queue length together,
  which is what one of the recorded examples does
- an internal system already exposes the right answer over an API and only needs adapting

## When not to use it

- **before trying the `prometheus` scaler.** This is the important one. If the signal can be
  exported as a metric — and most can — a Prometheus query is a `ScaledObject` field rather than a
  service to build, deploy, secure, monitor and keep alive
- for anything the `metrics-api`, `cron`, or `kubernetes-workload` scalers already cover
- if nobody will own it. An external scaler is a component in the scaling path: when it is down,
  KEDA cannot scale the workload it governs

## Notes

**The recorded opinion: the documentation is poor.** The original note reads *"doc meio merda"* —
"the docs are pretty crap". That is the reason this folder exists at all. The upstream page,
<https://keda.sh/docs/2.15/concepts/external-scalers/>, describes the gRPC interface but gives
little practical guidance on building, packaging and operating a scaler, which is why the notes
record three working implementations to read instead:

| Example | What it demonstrates |
|---|---|
| [dreamkast-external-scaler](https://github.com/cloudnativedaysjp/dreamkast-external-scaler) | a real production scaler from a conference platform — a complete Go implementation with deployment manifests |
| [keda-upstream-deployment-scaler](https://github.com/rafaelcalleja/keda-upstream-deployment-scaler) | scaling one workload based on the state of **another** Deployment — a dependency-driven scaler |
| [keda-error-threshold-and-queue-length-based-scaler](https://github.com/maniSbindra/keda-error-threshold-and-queue-length-based-scaler) | combining **two** signals — error rate and queue length — in a single scaling decision, which is the case built-in scalers cannot express |

Reading working code is the practical route here, and that is what the note is recording.

Nothing is deployed for this — the folder is documentation of a technique. Note also that the
documentation link is pinned to KEDA **2.15**; the interface is stable, but check the version in use
before following it literally.

---

[← KEDA](../README.md)
