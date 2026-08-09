[← Backup](../README.md)

# pv-migrate

<https://github.com/utkuozdemir/pv-migrate>

---

> **A migration tool, not a backup tool.** It copies one PVC to another, once. There is no
> schedule, no retention, no restore semantics.

## The problem it solves

Moving data between PersistentVolumeClaims — which sounds trivial and is not, because a PVC is
bound to a node, a storage class and often an access mode that cannot be changed in place.

The real cases:

| Situation | Why the volume has to move |
|---|---|
| **Changing StorageClass** | `storageClassName` is immutable on a PVC |
| **Resizing down** | expansion is supported, shrinking is not |
| Changing access mode | `ReadWriteOnce` to `ReadWriteMany` needs a new volume |
| Moving between clusters | different storage backends entirely |
| Rebalancing across zones | the volume is pinned to the wrong one |

It handles the awkward part: spinning up the pods, running rsync over the right path, and
choosing a strategy that works given the access modes involved.

## When to use it

- a one-off volume copy, especially a **StorageClass migration**
- moving persistent data during a cluster migration
- undoing a storage decision that turned out wrong

## When not to use it

- as a backup strategy. No schedule, no retention, no point-in-time recovery
- ongoing replication between clusters — [VolSync](../volsync/README.md)

## Why it is in this folder

Because the operation belongs to the same family: reading a volume and writing it somewhere
else safely. And because the situations that require it — an immutable field, a wrong storage
class — are the ones discovered at the least convenient moment.

---

[← Backup](../README.md)
