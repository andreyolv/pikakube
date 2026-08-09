[← Distributed key-value stores](../README.md)

# etcd

<https://github.com/etcd-io/etcd>
<https://github.com/etcd-io/etcd-operator>

---

## Why this one matters more than the others

**It is already running.** etcd is where Kubernetes stores every object in the cluster — every
Pod, Secret, ConfigMap and CRD. It is the only component whose failure means the cluster *stops*
rather than degrades.

That makes this page less about adopting etcd and more about understanding a dependency that
already exists.

| Property | Detail |
|---|---|
| Consensus | **Raft** — a strict majority must agree on every write |
| Consistency | **linearizable** reads and writes |
| Interface | gRPC, with a watch API |
| **Watches** | clients subscribe to key changes — this is how every Kubernetes controller works |
| Leases | keys with a TTL, renewed by a client — the basis of leader election |
| Scale | small data, high criticality |

The watch API is the part worth understanding, because it explains Kubernetes' architecture: a
controller does not poll the API server, it watches. Every operator in this repository is
ultimately a watcher on etcd, and controller count is therefore a real load consideration.

## When to use it directly

- **coordination** — leader election, distributed locks, service discovery
- configuration that must be strongly consistent, small, and read often
- as a dependency for something being built that needs consensus and should not implement it

## When not to use it

- **as an application database** — it is sized and tuned for small, critical, mostly-read state
- large values or high write throughput; every write is a consensus round trip
- caching — [`nosql/key-value/`](../../../nosql/key-value/README.md) is a different tool with a
  similar name

## The operational profile

The things that turn into incidents, in rough order of frequency:

| Concern | Detail |
|---|---|
| **Disk latency** | etcd is `fsync`-bound. Slow disks cause leader elections, and leader elections cause API server timeouts |
| **Database size** | the default quota is 2 GB; exceeding it puts the cluster into a **read-only alarm state** |
| Compaction | revisions accumulate; without compaction the size grows without bound |
| Defragmentation | reclaims space after compaction, and it briefly blocks |
| **Backups** | a snapshot is the only real recovery path for cluster state |
| Members | an **odd** number — three or five |
| Watch load | many controllers watching many objects is genuine cost |
| Large objects | a large ConfigMap or Secret is replicated by consensus on every write |

**Disk latency is the one that produces the confusing incident.** "The API server is slow" is very
often "etcd is waiting on `fsync`" — and the fix is storage rather than anything in the control
plane. See [`storage/`](../../../../site-reliability-engineering/storage/README.md).

The metric to alert on is `etcd_disk_wal_fsync_duration_seconds`. If its p99 exceeds roughly
10 ms, the cluster is on borrowed time.

## Backups

Worth stating separately because it is the one thing with no alternative recovery path.

```bash
etcdctl snapshot save snapshot.db
```

Every Kubernetes object exists only in etcd. Losing it without a snapshot means rebuilding the
cluster's entire state by hand — and a running control plane is not a backup, because the failure
that loses etcd loses it everywhere.

[Velero](../../../../site-reliability-engineering/backup/velero/README.md) backs up Kubernetes
resources through the API, which covers a different failure: an accidental deletion of objects,
rather than the loss of etcd itself. Both are worth having, and neither substitutes for the other.

## Notes

The [etcd-operator](https://github.com/etcd-io/etcd-operator) is for running etcd clusters *on*
Kubernetes — for an application that needs coordination, not for the control plane's own etcd,
which is managed by the cluster's installer.

For this platform etcd runs inside the [Kind](../../../../../clusters/kind-configs/) cluster and
nothing else in [`distributed/`](../../README.md) is deployed.

The practical takeaway is the disk-latency point. On a laptop-hosted Kind cluster, etcd shares a
disk with everything else — and a control plane that feels sluggish under load is usually this,
not the API server.

---

[← Distributed key-value stores](../README.md)
