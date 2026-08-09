[← KEDA](../README.md)

# KEDA HTTP add-on

<https://github.com/kedacore/http-add-on>
<https://github.com/kedacore/external-scalers>

---

## The problem it solves

[KEDA](../README.md) scales to zero by polling an external source and asking "is there work?". For
a queue that works, because the queue holds the work and can be measured while the workload is at
zero replicas.

HTTP has no queue. The work *is* the arriving request, and there is nothing to measure until it
arrives — at which point there are no Pods to serve it and the caller gets a connection error.
Scaling to zero and serving HTTP are in direct conflict unless something sits in the request path.

The HTTP add-on is that something:

| Component | Role |
|---|---|
| **Interceptor** | a proxy in front of the workload. It holds incoming requests, counts pending ones, and releases them when a Pod is ready |
| **External scaler** | exposes the interceptor's pending-request count to KEDA over the external-scaler gRPC protocol |
| **`HTTPScaledObject`** | the CRD you write; it wires the Service, the workload and the scaling bounds together |

The flow: a request arrives at zero replicas, the interceptor queues it and reports a non-zero
pending count, KEDA scales the workload from 0 to 1, the Pod becomes ready, the interceptor forwards
the held request. The caller experiences latency — the cold start — rather than an error.

Routing traffic through the interceptor is the price of admission. It is a new hop in the data path
for every request to every scaled service.

## When to use it

- an **internal or low-traffic HTTP service** that does not justify running around the clock —
  admin tools, dashboards, staging environments, per-branch preview deployments
- when the cold-start latency is acceptable to the caller, which usually means a human is waiting
  rather than a synchronous upstream service
- when KEDA is already deployed and adding an add-on is cheaper than adopting a second system

## When not to use it

- **for latency-sensitive production traffic.** A held request plus a scheduling decision plus
  container start plus readiness is seconds, not milliseconds
- if placing a proxy in the request path of a production service is not acceptable — it is another
  component that can fail, and its failure takes the service with it
- if the service already receives steady traffic. It will never scale to zero, and the interceptor
  is then pure overhead
- if what you want is scale-to-zero **without** a proxy hop on every request — see
  [KubeElasti](../../kubeelasti/README.md), which only involves its resolver while the workload is
  at zero

## Notes

Two recorded references: the add-on itself, <https://github.com/kedacore/http-add-on>, and
<https://github.com/kedacore/external-scalers>, the collection of KEDA's officially-maintained
external scalers — the add-on's scaler is one of them, which is why the two links are recorded
together.

**Deployed here**, via a Flux `HelmRelease` for the `keda-add-ons-http` chart, version `0.8.0`, into
the `keda` namespace, with `scaler.replicas: 3`.

Two things about that configuration are worth stating. It shares the `keda` namespace because the
add-on is not independent — it needs KEDA to do the actual scaling. And three scaler replicas is a
deliberate choice: the scaler and the interceptor are **in the request path**, so a single replica
makes them a single point of failure for every service behind them. That property is the main
argument against this approach and the main reason to over-provision it if you adopt it.

The version number is the other honest signal. A `0.x` release for a component that terminates
production HTTP traffic is a real consideration, and the add-on has been at `0.x` for a long time.

---

[← KEDA](../README.md)
