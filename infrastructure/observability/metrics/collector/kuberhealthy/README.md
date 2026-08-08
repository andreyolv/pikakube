[← Metrics collectors](../README.md)

# Kuberhealthy

<https://github.com/kuberhealthy/kuberhealthy>

---

## The problem it solves

Every other tool here reports on state that already exists. Kuberhealthy **creates** it.

It runs synthetic checks as real workloads — schedule a pod, resolve a DNS name, provision a
PVC, reach the API — and turns pass or fail into Prometheus metrics.

The gap it fills is the same one as
[network monitoring](../../../../network/monitoring/README.md): **passive metrics cannot see a
capability nobody exercised.** If nothing has created a PVC today, no metric anywhere says
whether provisioning still works. You find out when a StatefulSet needs one.

## When to use it

- proving that cluster **capabilities** work, not just that components are running
- catching broken provisioning, scheduling or DNS before a workload does
- custom checks — it runs any container you write as a check, which makes platform-specific
  probes straightforward

## When not to use it

- small clusters, where the checks cost more than the signal is worth
- you already probe the same paths another way
- as a substitute for application monitoring; this tests the platform, not the workloads

## The custom check angle

The generic checks are useful. The interesting use is writing your own for the platform's own
promises: can a data engineer's namespace still get a PVC, does the internal registry still
serve images, does the secret store still resolve.

Those are the failures that surface as "the platform is broken" at the worst moment, and
nothing else in this folder tests them.

---

[← Metrics collectors](../README.md)
