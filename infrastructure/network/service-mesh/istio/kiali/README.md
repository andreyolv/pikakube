[← Istio](../README.md)

# Kiali

<https://github.com/kiali/kiali>
<https://github.com/kiali/helm-charts>
<https://kiali.io/>

Console for [Istio](../README.md). Mesh context: [../../README.md](../../README.md)

---

## The problem it solves

Once a mesh is running, it produces a large amount of L7 telemetry and a large amount of
configuration — `VirtualService`, `DestinationRule`, `PeerAuthentication`,
`AuthorizationPolicy`. Both become hard to hold in your head.

Kiali gives two things that are difficult to get any other way:

- **the service graph** — a live map of which service calls which, with request rate, latency and error rate on each edge, derived from mesh telemetry with no instrumentation
- **configuration validation** — it inspects Istio objects and flags what is wrong or contradictory: a `VirtualService` pointing at a host that does not exist, overlapping rules, mTLS settings that conflict

The second is the underrated one. Istio configuration frequently fails silently — a policy
applies cleanly and does nothing because a selector matched nothing.

## When to use it

- alongside Istio, essentially always — it turns the mesh from opaque into inspectable
- when onboarding a team to an existing mesh, the graph is the fastest way to explain the system

## When not to use it

- without Istio; it reads Istio configuration and telemetry specifically
- as a general observability tool — it is mesh-scoped. Dashboards, long-term metrics and
  tracing belong in [`observability/`](../../../../observability/)

## Access note

Kiali shows traffic topology and configuration for the whole mesh, so exposing it is
effectively exposing an architecture diagram of the platform. Put it behind SSO, as with any
other cluster console.

---

[← Istio](../README.md)
