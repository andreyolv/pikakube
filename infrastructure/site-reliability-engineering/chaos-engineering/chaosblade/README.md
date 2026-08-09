[← Chaos engineering](../README.md)

# ChaosBlade

<https://github.com/chaosblade-io/chaosblade>
<https://github.com/chaosblade-io/chaosblade-operator>

---

## The problem it solves

Fault injection that is **not limited to Kubernetes**. From Alibaba, it works as a CLI on hosts
and as an operator in the cluster, with faults across several layers:

| Target | Examples |
|---|---|
| Kubernetes | pods, containers, nodes |
| Host | CPU, memory, disk, network, processes |
| **JVM** | method-level exceptions, delays, return values |
| Databases | connection and query faults |
| Cloud | provider-level disruptions |

The JVM row is the differentiator. Injecting an exception into a specific method of a running
Java application is something no Kubernetes-native tool does, and it tests error handling that
is otherwise unreachable without changing code.

## When to use it

- the estate is **not only Kubernetes** — VMs and cluster workloads need the same tooling
- **JVM-heavy** systems, where method-level fault injection tests error paths directly. Relevant for a data platform running Spark, Kafka and Trino
- you want a CLI for ad-hoc injection as well as declarative experiments

## When not to use it

- Kubernetes is the whole scope — [Chaos Mesh](../chaos-mesh/README.md) is more idiomatic there, with a broader Kubernetes fault set
- you want a catalogue and tracked results — [LitmusChaos](../litmus/README.md)

## Note

Documentation is substantially better in Chinese than in English, which is worth knowing before
committing time to it. The capability is real; the path to using it is rougher than the
alternatives if you cannot read the primary docs.

---

[← Chaos engineering](../README.md)
