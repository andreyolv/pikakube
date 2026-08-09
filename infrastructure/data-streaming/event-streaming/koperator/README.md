[← Event streaming](../README.md)

# Koperator

<https://github.com/banzaicloud/koperator>

---

## What it is

A Kafka operator from Banzai Cloud, built around a different assumption from Strimzi: brokers
are managed **individually** rather than as a StatefulSet.

That sounds minor and is not:

| | StatefulSet-based (Strimzi) | Koperator |
|---|---|---|
| Brokers | identical, ordinal-indexed | **individually configurable** |
| Per-broker storage | uniform | different volumes per broker |
| Per-broker resources | uniform | heterogeneous |
| Removing a specific broker | awkward — ordinals matter | direct |
| Rack awareness | supported | fine-grained |

The practical consequence is fine-grained rolling operations: upgrading, reconfiguring or
replacing **one** broker without touching the others, and running brokers with different
storage classes or sizes in the same cluster.

## When to use it

- brokers genuinely need to differ — heterogeneous storage or resources
- fine-grained control over rolling operations is required
- an existing Banzai/Cisco stack

## When not to use it

- **Strimzi covers it**, which it does for most deployments, and it has far more adoption and material
- project maintenance matters — check current activity, since Banzai Cloud's situation changed after the Cisco acquisition

## The honest positioning

Strimzi is the default Kafka operator, and this repository runs it. Koperator is worth knowing
for the specific case its design targets — per-broker heterogeneity — and worth checking the
maintenance status of before adopting.

## Related

Kafka in this repository runs on **Strimzi**, with topic and user governance — see
[`../README.md`](../README.md#6-how-this-applies-to-pikakube), including the restore procedure
that requires pausing the operator first.

That operator-pause detail applies here too, and to every operator-managed stateful workload —
[Velero](../../../site-reliability-engineering/backup/velero/README.md).

---

[← Event streaming](../README.md)
