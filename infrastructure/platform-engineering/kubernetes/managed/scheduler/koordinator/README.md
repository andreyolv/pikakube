[← Scheduler](../README.md)

# Koordinator

<https://github.com/koordinator-sh/koordinator>
<https://github.com/koordinator-sh/charts>

---

## The problem it solves

Koordinator is about **co-location**: running latency-sensitive services and batch workloads on the
same nodes without the batch work damaging the services.

The insight it is built on is that services request far more than they use, and that headroom is
paid for and idle. Koordinator measures actual usage, calculates the reclaimable difference, and
offers it to batch pods as a lower quality-of-service class — then protects the services with
runtime-level isolation: CPU suppression, memory eviction, CPU burst, and interference detection that
throttles batch work when a service starts to suffer.

So it is not only a scheduler. It is a scheduler plus a node agent doing continuous resource
arbitration.

## When to use it

- Large clusters where the gap between requests and usage is a significant cost
- Genuine mixed workloads: online services and offline batch on shared nodes
- You want reclaimed capacity used rather than merely reported
- The team can operate a node-level agent that manipulates cgroups

## When not to use it

- Small clusters; the reclaimable headroom does not justify the complexity
- Pure batch, or pure services — the co-location premise does not apply
- Where the right fix is right-sizing requests, which is simpler and free
- If a node agent adjusting cgroups under running workloads is not acceptable

## Notes

**Chart from a separate repository** — <https://github.com/koordinator-sh/charts>, distinct from the
project itself, which is why both links are recorded. Same pattern as
[Kubevious](../../dashboards/kubevious/README.md): chart issues and versioning live apart from the
application's.

Installed here with a `HelmRelease`, a `HelmRepository` and a namespace manifest, values empty.
Recorded as a link only.

**The honest framing of what it does.** Koordinator's value proposition is "use the capacity you are
already paying for and not using". That is real, and there is a much cheaper version of the same fix:
**right-size the requests**. If services request 4 CPU and use 0.5, correcting the manifests
recovers the same capacity with no controller, no node agent and no QoS classes.

Koordinator earns its place where that is not practicable — where requests must stay high to absorb
spikes, and the headroom exists precisely for bursts that occur rarely. Then reclaiming it for
preemptible batch work is genuinely clever. Adopting it *instead of* fixing requests is solving an
expensive problem with an expensive tool.

**The node agent is the part to evaluate carefully.** `koordlet` runs on every node and adjusts
cgroups for running containers: CPU suppression, memory limits, eviction under pressure. That is
powerful and it is a component with the ability to degrade production workloads if its interference
detection is wrong. It is the difference between this and a scheduler-only tool, and it is where the
risk lives.

Alibaba-originated, CNCF Sandbox. The comparison set is [Volcano](../volcano/README.md) for
job-centric batch and [YuniKorn](../yunikorn/README.md) for queue-centric capacity sharing —
Koordinator is the only one of the three whose primary concern is what happens **after** placement.

---

[← Scheduler](../README.md)
