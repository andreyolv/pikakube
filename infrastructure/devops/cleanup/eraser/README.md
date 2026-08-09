[← Cleanup](../README.md)

# eraser

<https://github.com/eraser-dev/eraser>

---

## The problem it solves

Nodes hoard images. Every tag ever pulled stays on disk until the kubelet decides otherwise, and
what the kubelet decides is driven by **disk pressure**, not by whether an image is safe to keep.
Two consequences follow:

| Symptom | Cause |
|---|---|
| Nodes run out of disk in the middle of the night | image layers accumulate faster than they are evicted |
| A known-vulnerable image sits on a node for months | nothing running uses it, so nothing removes it |

The second is the interesting one. An image that is no longer referenced by any Pod is still
present, still pullable from the local cache, and still counted by anything that inventories what
is on the node. A CVE report against it does not go away because the Deployment was updated.

eraser runs a job across the nodes that lists the images present, decides which are removable, and
removes them. It works in two modes:

- **Manual** — an `ImageList` resource naming images (or `*`) to remove
- **Scheduled scanning** — on an interval, a scanner (Trivy by default) evaluates the images on
  each node against a vulnerability threshold, and the remover deletes those that fail and are not
  in use

Images backing running containers are excluded, as is anything on the configured exclusion list.

## When to use it

- **Node disk usage is a recurring operational problem**, and raising the kubelet thresholds is
  treating the symptom
- unused vulnerable images on nodes are flagged by a compliance or posture tool and have to
  actually disappear
- a cluster with high image churn — CI building a new tag per commit and running it somewhere is
  the classic generator
- long-lived nodes; on a fleet that is replaced weekly the problem largely solves itself

## When not to use it

- **Before checking what the kubelet already does.** Kubelet image garbage collection is built in
  and driven by `imageGCHighThresholdPercent` / `imageGCLowThresholdPercent`, and recent Kubernetes
  versions also support `imageMaximumGCAge`, which evicts images unused for longer than a set
  period. For pure disk-space management that is often enough, costs nothing, and needs no
  controller
- if the driver is *vulnerabilities in images that are actually running* — that is a registry and
  supply-chain problem, not a node problem, and belongs in the security discipline
- on clusters where nodes are immutable and short-lived; there is nothing to accumulate
- if aggressive removal would hurt: eraser deleting a base image means the next Pod scheduled there
  re-pulls it. On a slow or rate-limited registry that trade is not free

## Notes

The only recorded reference is the repository itself: <https://github.com/eraser-dev/eraser>.

The project began life inside Azure and now lives under the `eraser-dev` organisation as a
CNCF-adjacent effort. There are no manifests for it in this repository — unlike
[kube-cleanup-operator](../kube-cleanup-operator/README.md) and [mayfly](../mayfly/README.md), it is
mapped rather than deployed.

The distinction worth keeping in mind when reading this folder: eraser is the only one of the three
that operates on **node state**. The other two operate on **API objects**. A cluster can need one
and not the other, and the failure they prevent is different — a full disk versus an unreadable
`kubectl get pods`.

---

[← Cleanup](../README.md)
