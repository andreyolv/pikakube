[← Network monitoring](../README.md)

# kubenurse

<https://github.com/postfinance/kubenurse>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

Passive metrics cannot see a network path that nobody used. A cluster looks healthy while
traffic between two specific nodes is silently broken, and you find out when a pod happens
to land on the wrong node.

kubenurse runs as a **DaemonSet** and continuously probes, from every node:

- **every other node** — producing an N×N reachability matrix
- the **API server**
- **DNS**
- the **ingress**, following the full external round trip back into the cluster

Results are exposed as Prometheus metrics, so failures become alertable before a workload
discovers them.

## When to use it

- clusters with enough nodes that one pair can break independently of the rest
- after a CNI change, an MTU adjustment or a security group edit — it tells you immediately which pairs stopped working
- as the standing proof that the cluster network works, rather than an assumption

## When not to use it

- single-node or throwaway clusters — there is no matrix to measure
- when what you actually want is probing an **arbitrary external endpoint**; the blackbox exporter under [`observability/`](../../../observability/README.md) is the general-purpose version of the same idea

## Alerting note

Alert on **sustained failure of a specific pair**, over a window — not on individual probe
failures. A single transient drop is normal and paging on it trains people to ignore the
alert.

---

[← Network monitoring](../README.md)
