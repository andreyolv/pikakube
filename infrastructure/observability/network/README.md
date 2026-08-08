[← Observability](../README.md)

# Network observability

Seeing the network layer specifically — flows, drops, and DNS — rather than the applications
riding on it.

Tools covered: [`retina`](retina/) · [`netobserv`](netobserv/)

---

## Where this sits

Networking has three folders and they answer different questions:

| Question | Where |
|---|---|
| Is the network path working at all? | [`network/monitoring/`](../../network/monitoring/README.md) — synthetic probing |
| Why is *this* connection failing? | [`network/troubleshooting/`](../../network/troubleshooting/README.md) — a method |
| **What is the flow-level picture over time?** | **here** |

This folder is about **continuous** network visibility: which pods talk to which, how much,
what is being dropped and why, and how DNS behaves — as metrics and flows you can query
later, not a capture you run during an incident.

## The problem it solves

Kubernetes networking is opaque by default. A `NetworkPolicy` drops a packet and nothing
records it — the client sees a timeout, and there is no signal anywhere saying "this was
denied by policy".

eBPF-based network observability closes that: flow logs, drop reasons, per-pod traffic, DNS
latency and failures, all without changing a single application.

The two questions it answers that nothing else does:

- **who is actually talking to whom?** — the real dependency graph, as opposed to the diagram
- **why was this dropped?** — policy denial, conntrack exhaustion, or the network itself

## The tools in this folder

| Tool | Role | Shines when | Detail |
|---|---|---|---|
| **Retina** | Microsoft's eBPF network observability, CNI-agnostic | you want flow visibility **without adopting Cilium** — it works on any CNI | [→](retina/) |
| **NetObserv** | the OpenShift network observability operator, based on eBPF and Flow Collector | you are in the OpenShift ecosystem, or want a mature flow pipeline with a console | [→](netobserv/) |

### The alternative you may already have

If [Cilium](../../network/cni/cilium/) is the CNI, **Hubble** provides flow visibility with
nothing extra to install — and it is the most mature option of the three.

Both tools here exist mainly for the case where Cilium is *not* the CNI. That is worth
checking before installing anything: the answer may already be running.

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Installing a flow tool when Cilium is already the CNI | Hubble covers it, better | check first |
| Capturing all flows with no retention plan | flow data volume is very large | sample and scope by namespace |
| Using flow logs as a security audit trail | they show traffic, not intent or identity | [audit logs](../../security/2-cluster/audit/) and runtime security |
| Treating it as a debugging tool | it is a continuous signal; ad-hoc debugging is [netshoot](../../network/troubleshooting/netshoot/) | use it for patterns, not for one-off checks |

## How this applies to pikakube

**Retina** is mapped, with real problems recorded in its README — it is the CNI-agnostic
option, which is what makes it interesting on a Kind cluster running kindnet.

Neither is deployed.

---

[← Observability](../README.md)
