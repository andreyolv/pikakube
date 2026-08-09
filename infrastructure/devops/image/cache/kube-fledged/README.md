[← Image caching](../README.md)

# kube-fledged

<https://github.com/senthilrch/kube-fledged>

---

## The problem it solves

**Pre-pulling a declared set of images onto declared nodes, and keeping them there.** A pod whose
image is already in the node's content store starts in seconds instead of minutes; kube-fledged
makes that a declarative resource rather than a trick.

The API is one CRD:

```yaml
apiVersion: kubefledged.io/v1alpha2
kind: ImageCache
spec:
  cacheSpec:
  - images:
    - ghcr.io/jitesoft/nginx:1.23.1        # every node
  - images:
    - us.gcr.io/k8s-artifacts-prod/cassandra:v7
    nodeSelector:
      tier: backend                        # only these nodes
  imagePullSecrets:
  - name: myregistrykey
```

The controller creates pull jobs on the matching nodes, tracks the cache status in the resource,
and refreshes on a configurable interval. Compared with the folk alternative — a `DaemonSet` that
references the image and sleeps — it handles many images, per-node targeting, private registries
and status reporting, in one resource.

| Capability | Detail |
|---|---|
| Declarative | an `ImageCache` resource, reconciled |
| Node targeting | a `nodeSelector` per image group |
| Private registries | `imagePullSecrets` on the cache spec |
| Refresh | periodic, so a moved tag can be re-pulled |
| Status | which nodes have which images, reported on the resource |

## When to use it

- **cold-start latency on a known, small set of images** — the ones that hurt: large runtimes, ML
  base images, anything with a multi-gigabyte layer
- nodes that are replaced constantly: autoscaling groups, **spot instances**, preemptible VMs
- images that must be present before a workload can be scheduled, where waiting on a pull is
  unacceptable
- clusters with heterogeneous node pools, where only some nodes need a given image

## When not to use it

- when the problem is **upstream availability** rather than latency — that is
  [kube-image-keeper](../kube-image-keeper/README.md)
- when the problem is registry fan-out across hundreds of nodes —
  [`../../p2p-mirror/`](../../p2p-mirror/README.md)
- to pre-pull everything: node disk is finite, and the kubelet's image garbage collection will
  start evicting under disk pressure — possibly the images just pre-pulled
- with mutable tags, where a pre-pulled `:latest` becomes a *stuck* `:latest` that
  `IfNotPresent` will never refresh
- when smaller images would remove the problem entirely, which is cheaper and permanent

## Notes

Recorded link:

- <https://github.com/senthilrch/kube-fledged> — the project. It is a single-maintainer operator
  with a long history, and the release cadence is slow; the CRD is still `v1alpha2`. It works, and
  it is worth checking recent activity before depending on it in production.

What is configured here: a Flux `HelmRelease` at chart version **v0.10.0**, in its own namespace,
plus an `example/imagecache.yaml` demonstrating both targeting modes — a list of images cached on
every node, and a list constrained by `nodeSelector: tier: backend`, with `imagePullSecrets` for
private repositories. The example is taken from upstream and the comments in it explain each
field, which makes it the right thing to copy from.

**How this relates to the `daemonset.yaml` in the parent folder.** That file is the manual version
of the same idea: an `image-prepull` `DaemonSet` running `ubuntu:20.04` with `sleep 3600`,
`tolerations: operator: Exists` so it schedules everywhere, and `nodeSelector: spot: "true"` so it
targets spot nodes. It works — Kubernetes must pull the image to run the pod, so the image is now
cached — and it costs one running pod per node, per image. kube-fledged is the same trick made
declarative and multi-image; below two or three images the `DaemonSet` is genuinely less to
operate.

The two things to size before deploying it:

- **node disk.** Cached images consume it, and the kubelet evicts images under pressure. Pre-pull
  the images whose cold pull actually hurts, not the catalogue.
- **the refresh interval.** Each refresh is a synchronised pull across the selected nodes, which
  is a small version of the pull storm the tool exists to avoid.

## Where it fits here

The latency answer in [`cache/`](../README.md), where
[kube-image-keeper](../kube-image-keeper/README.md) is the availability answer and
[k8s-image-swapper](../k8s-image-swapper/README.md) the redirection one. The `nodeSelector: spot`
in the sibling `daemonset.yaml` is the clearest statement of why it matters here: spot nodes are
replaced constantly, so pull time is paid constantly.

---

[← Image caching](../README.md)
