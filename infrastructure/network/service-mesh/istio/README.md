[← Service mesh](../README.md)

# Istio

<https://github.com/istio/istio>
<https://istio.io/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

The most complete service mesh available: mTLS with workload identity, fine-grained traffic
routing, multi-cluster topologies, an extension model, and L7 telemetry between every pair
of services.

If a mesh feature exists anywhere, it probably exists here. That is both the reason to pick
it and the reason not to.

## Two deployment models

| | Sidecar | **Ambient** |
|---|---|---|
| Where the proxy runs | injected into every pod | per-node component for L4/mTLS, plus an L7 proxy only where needed |
| Overhead | per pod | per node |
| Upgrades | restart every workload | restart infrastructure |
| Batch workloads | need explicit exclusion or Jobs never complete | not affected — the pod spec is untouched |
| Maturity | long-established | newer |

Ambient is the answer to the two most common complaints about meshes — per-pod cost, and
sidecars breaking Jobs. The repo maps it separately under
[`istio-ambient-mode/`](../istio-ambient-mode/).

## When to use it

- the requirement genuinely includes **fine-grained traffic policy** — weighted routing, mirroring, fault injection, per-route rules
- **multi-cluster** mesh topologies
- you need the extension ecosystem, or an organisation-wide standard already built on Istio

## When not to use it

- the requirement is "mTLS and retries" — [Linkerd](../linkerd/) delivers that with far less to operate
- a small cluster where the feature list exceeds anything you will configure
- the team has no capacity to absorb a new debugging surface; a 503 can now originate in four different places

## Related

- **Kiali** — service graph and configuration validation: [`kiali/`](kiali/)
- **Kmesh** — eBPF-based sidecarless mesh, a different take on the same problem: <https://github.com/kmesh-net/kmesh>

---

[← Service mesh](../README.md)
