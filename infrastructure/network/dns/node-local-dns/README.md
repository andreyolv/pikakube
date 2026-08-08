[← DNS](../README.md)

# NodeLocal DNSCache

<https://github.com/kubernetes/kubernetes/tree/master/cluster/addons/dns/nodelocaldns>
<https://github.com/deliveryhero/helm-charts>
<https://kubernetes.io/docs/tasks/administer-cluster/nodelocaldns/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

Two related problems, both of which appear as "DNS is flaky":

**1. Sporadic 5-second timeouts.** A known race in the Linux conntrack handling of UDP DNS
causes occasional lookups to hang until the client times out and retries. It is intermittent,
looks random, and is one of the harder symptoms to attribute.

**2. CoreDNS under load.** Every pod on every node queries the central CoreDNS Service. At
scale — amplified by the [`ndots:5`](../README.md#the-ndots5-trap) expansion turning one
lookup into four — that is a lot of traffic to a handful of pods.

NodeLocal DNSCache runs as a **DaemonSet**: a cache on each node answers locally over TCP to
the upstream, which removes the conntrack race and absorbs most of the query volume.

## When to use it

- **sporadic 5s DNS latency** with no other explanation — this is the standard fix
- CoreDNS is visibly loaded, or its pods are a scaling concern
- large clusters, or workloads making many external calls

## When not to use it

- small clusters, where it is a DaemonSet and a moving part earning nothing
- before checking the cheaper fixes — a trailing dot on hostnames, or lowering `ndots` per workload, may remove the load entirely

## Order of operations

Fix `ndots` first if the problem is *slow* external lookups. Add this cache if the problem is
*intermittent timeouts*, or if the volume itself is the issue. They address different causes
and are frequently confused.

---

[← DNS](../README.md)
