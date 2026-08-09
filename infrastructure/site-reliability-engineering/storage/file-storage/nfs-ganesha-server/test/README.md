[← NFS Ganesha server](../README.md)

# Provisioner smoke test

<https://github.com/kubernetes-sigs/nfs-ganesha-server-and-external-provisioner/tree/master/docs>

The two-object check that
[`nfs-server-provisioner`](../README.md) actually provisions `ReadWriteMany` volumes.

---

## The problem it solves

A storage provisioner that is installed is not a storage provisioner that works. The Helm release
reconciles, the pods are `Running`, the StorageClass appears — and none of that proves a PVC will
bind or that a pod can write to what it gets.

This is the smallest test that proves the whole path end to end:

| Step | What it proves |
|---|---|
| A PVC asking for `ReadWriteMany` on `storageClassName: nfs` | the StorageClass exists and the provisioner is watching |
| The PVC reaching `Bound` | Ganesha created an export and a PV was written |
| A pod mounting it | the NFS mount succeeds on the node — client packages, network, Service DNS |
| `touch /mnt/SUCCESS` succeeding | the export is writable, and permissions are not in the way |
| The pod reaching `Completed` | all of the above, in one observable state |

Each of those is a distinct failure mode, and the test distinguishes them by where it stops. A
PVC stuck `Pending` is a provisioner problem. A PVC `Bound` with a pod stuck in
`ContainerCreating` is a mount problem — usually a missing NFS client on the node, or the Service
not resolving. A pod that starts and then fails is a permissions problem.

That last distinction is the one worth having a test for, because in production it appears as an
application bug.

## When to use it

- **Immediately after installing the provisioner**, before any real workload depends on it.
- **After changing the backing storage class or the backing PVC size** — the parts of
  [the parent configuration](../README.md#notes) that decide whether anything can be provisioned
  at all.
- **After a cluster or node upgrade**, since the NFS mount depends on packages and kernel
  behaviour on the node, not only on the pod.
- **When diagnosing a failure**, as the minimal reproduction: if this passes, the provisioner is
  fine and the problem belongs to the workload.
- As the pattern for testing **any** storage class. The shape — claim, mount, write, exit —
  transfers unchanged to [Longhorn](../../../block-storage/longhorn/README.md),
  [csi-driver-nfs](../../csi-driver-nfs/README.md) or a cloud driver.

## When not to use it

- **As evidence that RWX works across nodes.** One pod mounting a volume proves the mount path,
  not concurrent access. On a single-node cluster it proves even less — see
  [file-storage](../README.md).
- **As a performance test.** A single `touch` says nothing about throughput, latency or
  behaviour under concurrency, and NFS is exactly where those differ from expectation.
- **As a durability test.** It does not survive a restart, exercise the backing PVC's failure
  behaviour, or test what happens when the Ganesha pod moves — which is
  [the parent README's](../README.md#the-cost-which-is-not-hidden) main warning.
- **Left running in a cluster.** It is a one-shot job-shaped pod; delete it and its PVC when the
  check passes, or the export stays allocated against a backing PVC that is only 4Gi.

## Notes

**What is here.**

| Object | Detail |
|---|---|
| `PersistentVolumeClaim` | `nfs`, `storageClassName: nfs`, `accessModes: [ReadWriteMany]`, `resources.requests.storage: 1Mi` |
| `Pod` | `write-pod`, `busybox:1.37.0`, `restartPolicy: Never`, mounting the PVC at `/mnt` |

The pod's command is the entire test:

```
touch /mnt/SUCCESS && exit 0 || exit 1
```

Exit code 0 means the volume was mounted and is writable. Exit code 1 means it was mounted and is
not. The pod not starting at all means the mount failed, which is a third outcome — so
`kubectl get pod write-pod` distinguishes all three without reading logs.

This is the upstream test pattern, and the `SUCCESS` filename is conventional across the
kubernetes-csi and sig-storage example suites. Recognising it saves time when reading other
projects' examples.

**`1Mi` is deliberate and slightly misleading.** It is small because the test needs no space, and
it binds because [the provisioner does not enforce per-volume size](../README.md#capacity-is-real-here-unlike-most-nfs-provisioning)
— every export is a subdirectory of one backing PVC. A `1Mi` claim and a `100Gi` claim would both
bind against the same 4Gi backing volume, and neither number constrains anything. The test
therefore also quietly demonstrates that PVC sizes on this provisioner are documentation.

**`accessModes: [ReadWriteMany]` is the meaningful field.** It is what the whole tool exists to
provide, and it is what would fail against a block StorageClass — see
[block-storage §1.1](../../../block-storage/README.md#11-rwo-is-the-whole-story). Requesting RWX
here is the assertion being tested, even though only one pod mounts it.

**`restartPolicy: Never` matters** for a test pod. With the default `Always`, a failure would
loop and the pod would sit in `CrashLoopBackOff`, which reads as an ongoing problem rather than a
recorded result. `Never` leaves the pod in `Succeeded` or `Failed` — a permanent, readable
verdict.

**The PVC has no namespace** in the manifest, so both objects land in whatever namespace they are
applied to. Fine for a manual test; worth knowing before applying it somewhere unexpected.

**Extending it to actually test RWX** would mean two pods with anti-affinity on different nodes,
one writing and one reading, which is the check that matters on a real multi-node cluster and
which cannot be performed on Kind at all. That gap is the same one recorded throughout this
folder: the sandbox verifies the manifests, not the properties.

---

[← NFS Ganesha server](../README.md)
