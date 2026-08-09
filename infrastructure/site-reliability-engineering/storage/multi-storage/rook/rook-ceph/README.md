[← Rook](../README.md)

# rook-ceph (operator)

<https://github.com/rook/rook>
<https://artifacthub.io/packages/helm/rook/rook-ceph>

Chart values: <https://github.com/rook/rook/blob/master/deploy/charts/rook-ceph/values.yaml>

Upstream examples: <https://github.com/rook/rook/tree/master/deploy/examples>

The first of the two [Rook](../README.md) deployment shapes. Its counterpart is
[`../rook-ceph-cluster/`](../rook-ceph-cluster/README.md).

---

## The problem it solves

This chart installs **the machinery, and no storage**. It is the simpler of the two shapes and
must exist first.

What it provides:

| Component | Role |
|---|---|
| **CRDs** | `CephCluster`, `CephBlockPool`, `CephFilesystem`, `CephObjectStore`, and the rest |
| **The operator** | a single Deployment that watches those CRDs and reconciles Ceph to match |
| **Ceph-CSI drivers** | the RBD and CephFS provisioners, attachers and node plugins |
| **Discovery DaemonSet** | finds available block devices on each node (optional) |
| RBAC, service accounts, PSA labels | the permissions all of the above need |

After installing this chart you have: no MONs, no OSDs, no pools, no StorageClasses, and nothing
storing anything. What you have is a cluster that **understands** `CephCluster` as a kind, and a
controller waiting for one to appear.

That is exactly the right split, and it is not an accident of packaging.

### Why the two charts are separate

This is the pattern behind most Kubernetes operators, and Rook is a clear example of why it
exists:

| | Operator (here) | [Cluster](../rook-ceph-cluster/README.md) |
|---|---|---|
| Installs | CRDs, controller, CSI drivers | `CephCluster`, pools, filesystems, storage classes |
| Stateful | no — it can be restarted freely | **yes** — this is the data |
| Upgrade risk | low; the controller reconnects | high; it touches every OSD |
| Count per cluster | one | one or more |
| Deleting it | leaves the data, breaks reconciliation | **can destroy the data** |
| Lifecycle | follows Rook releases | follows your data, and moves more slowly |

Keeping them apart means the controller can be upgraded, restarted or reinstalled without
touching a `CephCluster` — and, more importantly, that a Flux prune or a Helm uninstall of the
operator does not delete the CRs holding the storage.

The ordering constraint is absolute: **CRDs must exist before any `Ceph*` resource can be
created.** Applying both at once produces a `CephCluster` the API server rejects because the kind
is unknown, and Flux will retry until the CRDs land. Explicit dependency ordering avoids the
noise.

### Upgrades happen here, and they are not trivial

Because this chart carries the operator and the CRDs, **a Rook version upgrade is an upgrade of
this chart**. Two rules that matter:

- **Do not skip minor versions.** Rook supports upgrading one minor release at a time, and the
  operator performs migrations between them.
- **The Ceph version is separate.** The Ceph image is set in the `CephCluster` resource, in the
  other chart. Rook and Ceph are upgraded independently, in that order, and a supported
  combination matters.

Helm's handling of CRDs is the other sharp edge: Helm does not upgrade CRDs on `helm upgrade` by
default. Rook's chart manages this, but it is worth knowing that CRD drift is possible and that
the symptom is a field in an example manifest being silently ignored.

## When to use it

- **Always, and first**, when Rook is being used at all. There is no configuration in which this
  chart is skipped.
- **On its own, briefly**, to verify the operator starts, the CRDs register and the CSI pods come
  up — before declaring a `CephCluster` and committing disks to it.
- When running **multiple Ceph clusters** in one Kubernetes cluster: one operator, several
  `CephCluster` resources.
- When connecting to an **external Ceph cluster** that is already run outside Kubernetes. This
  chart plus a `CephCluster` in external mode gives you the CSI drivers and StorageClasses
  without Rook operating any daemons — a genuinely good use of Rook that is easy to overlook.

## When not to use it

- **Expecting storage from it.** It provisions nothing on its own. A common first confusion is
  installing this chart, seeing every pod `Running`, and wondering why there is no StorageClass.
- **Alongside another Ceph management tool** on the same cluster. Rook expects to own the daemons
  it manages; `cephadm` and Rook reconciling the same cluster will fight.
- **On a cluster where the CSI node plugins cannot run privileged.** Mounting RBD and CephFS
  requires it, and no configuration avoids that.
- **Installed at the same time as the cluster chart**, without ordering. The CRDs must land
  first.

## Notes

**How it is deployed here.** A Flux `HelmRelease` named `rook-ceph` in the `rook-ceph` namespace,
pinned to chart version `1.16.0`, sourced from the `rook-release` `HelmRepository`, with an empty
values block and the upstream values file referenced in a comment.

An empty values block is more defensible here than in most of this repository, because the
operator chart's defaults are genuinely reasonable — this chart mostly installs controllers, and
the decisions live in the other one. The values that do matter in a real deployment:

| Value | Why |
|---|---|
| `csi.enableRbdDriver` / `enableCephfsDriver` | turn off what you do not use; each is a controller plus a DaemonSet |
| `csi.provisionerReplicas` | 2 by default; 1 on a single-node cluster avoids a permanently pending pod |
| `enableDiscoveryDaemon` | off by default; needed if you want automatic device discovery |
| resource requests | the CSI DaemonSets run on every node and the defaults are not free |
| `monitoring.enabled` | Prometheus rules for the operator |
| `logLevel` | the operator's log is the first place to look when a CR does not reconcile |

**The `example/` folder here holds a `CephBlockPool`**, which strictly belongs to the cluster
rather than to the operator — a `CephBlockPool` requires a `CephCluster` to exist. It is
duplicated identically in
[`../rook-ceph-cluster/example/`](../rook-ceph-cluster/README.md), and reading it alongside this
chart is a reasonable way to see what the CRDs installed here make possible:

- `failureDomain: host` — replicas are placed on distinct **hosts**, which is the correct setting
  on a multi-node cluster and meaningless on one node.
- `replicated.size: 3` — three copies, so usable capacity is one third of raw.
- `hybridStorage` with `primaryDeviceClass: ssd` and `secondaryDeviceClass: hdd` — the primary
  copy on SSD for latency, the rest on HDD for cost. It requires device classes that actually
  exist in the CRUSH map, which means real mixed hardware.

None of those conditions hold in a Kind cluster, which is the caveat recorded throughout
[multi-storage](../../README.md).

**What to install alongside it.** The `rook-ceph-tools` deployment from
[the upstream examples](https://github.com/rook/rook/tree/master/deploy/examples) — a pod with
the `ceph` CLI pointed at the cluster. It is the primary diagnostic interface for everything Rook
manages, and it is not part of this chart. A Rook installation without the toolbox is a Ceph
cluster you cannot inspect.

**Namespace.** Both charts land in `rook-ceph`, which is Rook's convention and worth keeping.
The operator can watch other namespaces, but the defaults, the examples and most documentation
assume this one.

---

[← Rook](../README.md)
