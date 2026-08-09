[← Event-driven](../README.md)

# KubeElasti

<https://github.com/KubeElasti/KubeElasti>

---

## The problem it solves

**Scale-to-zero for HTTP services**, which is the case [KEDA](../keda/README.md) alone cannot cover:
at zero replicas there is no metric that says "a request just arrived", and the caller gets a
connection refused rather than a slow response.

The [KEDA HTTP add-on](../keda/keda-http/README.md) solves it by putting an interceptor proxy in
front of the service permanently. KubeElasti solves it differently, and the difference is the
reason it is mapped here:

| State | What handles traffic |
|---|---|
| **Scaled up** (≥ `minTargetReplicas`) | the workload itself — **KubeElasti is not in the request path** |
| **Scaled to zero** | the resolver holds the request, triggers scale-up, and proxies it once the Pod is ready |

The controller switches the Service's endpoints between the workload and its resolver depending on
the state. So the proxy hop exists only during a cold start, and a service receiving steady traffic
pays nothing.

### How it decides

An `ElastiService` names a workload and a Service, and carries triggers:

| Field | Meaning |
|---|---|
| `scaleTargetRef` | the workload to scale |
| `service` | the Service whose endpoints get switched |
| `minTargetReplicas` | the replica count to restore on wake-up |
| `cooldownPeriod` | how long the trigger must stay below threshold before scaling to zero |
| `triggers` | currently Prometheus queries — the signal for **scaling down to zero** |
| `autoscaler` | hands off to KEDA or an HPA for scaling **above** the minimum |

The division of labour is deliberate and worth stating: KubeElasti owns the **0 ↔ 1** transition,
and delegates **1 → N** to whatever autoscaler already exists. It complements KEDA rather than
replacing it.

## When to use it

- HTTP services that should not run around the clock, where the proxy overhead of the KEDA HTTP
  add-on on hot traffic is the objection
- internal tools, dashboards, preview environments, per-team staging deployments — anything with
  long idle periods and a human on the other end of the first request
- when KEDA is already handling scaling above one replica and only the zero case is missing

## When not to use it

- **for latency-critical services.** Cold start is cold start regardless of implementation
- for non-HTTP workloads — queue consumers scale to zero perfectly well with plain
  [KEDA](../keda/README.md) and need none of this
- where a controller mutating Service endpoints is unacceptable. That mechanism is what makes the
  approach work and it is also its sharpest edge: a bug there affects traffic routing, not just
  scaling
- on a cluster without Prometheus. The triggers are Prometheus queries; without a metrics stack
  there is no scale-down signal

## Notes

The only recorded reference is the repository: <https://github.com/KubeElasti/KubeElasti>.

The CRD group is `elasti.truefoundry.com` — the project originated at TrueFoundry and later moved to
its own `KubeElasti` organisation. The old group name persists in the API, which is worth knowing
when searching for documentation, since older material refers to it as "Elasti".

**Deployed here**, via a Flux `HelmRelease` sourced from an `OCIRepository` — one of the tools in
this discipline that supports OCI, unlike [KEDA](../keda/README.md).

**Two `ElastiService` definitions are recorded**, and comparing them is instructive:

| File | Trigger source | Autoscaler handoff |
|---|---|---|
| `elastiservice.yaml` | Istio sidecar request rate — `envoy_http_downstream_rq_total{container="istio-proxy"}`, threshold `0.01` | `keda`, via a `ScaledObject` named `target-scaled-object` |
| `test/elastiservice.yaml` | NGINX ingress request rate — `nginx_ingress_controller_requests`, threshold `0.1` | none — scale-to-zero only |

Both use `or vector(0)`, which is the detail that matters: when no requests have been served, the
rate query returns **no series at all**, not zero. Without `or vector(0)` the trigger evaluates to
nothing and the controller cannot tell "no traffic" from "no data". Getting this wrong is the most
common way a Prometheus-driven scale-to-zero setup silently fails to scale down.

The test example carries `kustomize.toolkit.fluxcd.io/reconcile: disabled`, which tells Flux to
create the resource and then leave it alone — appropriate for something being poked at by hand
during an experiment, and a habit worth keeping out of anything permanent.

**A working test environment is recorded** under `test/`: a namespace, a Deployment, a Service and
an Ingress, so the wake-up behaviour can be driven with a real HTTP request rather than reasoned
about.

**Observability is wired up** under `observability/`, with a Grafana dashboard and folder as
resources, plus `metrics.md` recording how to reach the metrics endpoints directly:

```
k port-forward svc/kubeelasti-operator-controller-service 8013
k port-forward svc/kubeelasti-resolver-service 8013
```

then `http://127.0.0.1:8013/metrics`. The note also records the PromQL used to discover what the
project actually exports, which is the practical way to explore an undocumented metrics surface:

```
sort_desc(count by (__name__) ({__name__ =~ "elasti_.*"}))
```

Two port-forwards on the same local port is not an oversight — the operator and the resolver are
separate components with separate metrics, and you look at one at a time.

---

[← Event-driven](../README.md)
