[← Network](../README.md)

# Traffic analyzer

Conceptual reference for the `traffic-analyzer/` folder: seeing the **actual traffic**
flowing between pods, not metrics about it.

Tools covered: [`kubeshark`](kubeshark/)

## Contents

1. [Where this sits](#1-where-this-sits)
2. [The tools in this folder](#2-the-tools-in-this-folder)
3. [Alternatives already in the repo](#3-alternatives-already-in-the-repo)
4. [Anti-patterns](#4-anti-patterns)
5. [How this applies to pikakube](#5-how-this-applies-to-pikakube)

---

## 1. Where this sits

Three different questions, three different folders:

| Question | Folder |
|---|---|
| Is the network working at all? | [`monitoring/`](../monitoring/README.md) — synthetic probing |
| Why is *this* connection failing? | [`troubleshooting/`](../troubleshooting/README.md) — a layered method |
| **What is actually on the wire?** | **this folder** |

A traffic analyzer is what you reach for when the method in `troubleshooting/` has narrowed
the problem down and you now need to see the payload — which headers were sent, what the
service really answered, which calls a pod is making that nobody documented.

It is the cluster-wide, always-on version of running `tcpdump` inside a pod. That capability
is powerful and, for the same reason, sensitive: it observes real traffic, including
credentials and personal data.

## 2. The tools in this folder

| Tool | What it does | Detail |
|---|---|---|
| **Kubeshark** | captures traffic cluster-wide and presents it as protocol-aware flows — HTTP, gRPC, DNS, Kafka, Redis — with a UI, rather than raw packets | [→](kubeshark/) |

## 3. Alternatives already in the repo

Depending on what you actually need, something else may already be installed:

| Need | Where |
|---|---|
| Flow-level visibility with an eBPF dataplane | **Hubble**, part of [Cilium](../cni/cilium/) |
| Pod-level packet capture, ad hoc | `tcpdump` inside [netshoot](../troubleshooting/netshoot/) |
| L7 telemetry between meshed services | [`service-mesh/`](../service-mesh/README.md), and Kiali for Istio |
| Aggregated metrics rather than individual flows | [`observability/`](../../observability/) |

If Cilium is already the CNI, Hubble covers a large part of this without adding another
component — worth checking before installing anything here.

## 4. Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Leaving cluster-wide capture running permanently | it observes real traffic, including secrets and personal data, and is an obvious target | enable it for an investigation, then turn it off |
| Capturing in production without agreement | there are legal and privacy implications, not just technical ones | agree the scope first, and limit it by namespace |
| Reaching for packet capture first | most problems are DNS, endpoints or policy, and are answered in seconds | walk [`troubleshooting/`](../troubleshooting/README.md) first |
| Assuming capture is free | it costs CPU and memory on every node it runs on | scope it to the namespaces under investigation |

## 5. How this applies to pikakube

Mapped rather than run. On a single-node local cluster, `tcpdump` inside
[netshoot](../troubleshooting/netshoot/) covers the same ground with nothing to install.

The value of a dedicated analyzer appears when the traffic is spread across many nodes and
namespaces and you cannot guess in advance where to attach.

---

[← Network](../README.md)
