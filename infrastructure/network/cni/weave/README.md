[← CNI](../README.md)

# Weave Net

<https://github.com/weaveworks/weave>

Context and comparison against the other CNIs: [../README.md](../README.md)

---

> **Historical reference, not a candidate.** Weaveworks ceased operations in 2024 and the
> original project is no longer maintained by the company. A community fork exists, but new
> clusters should choose something else.

## The problem it solved

A VXLAN overlay CNI that was popular for being easy to install — a single manifest, no
external datastore, automatic mesh formation between nodes. It also offered encryption
between nodes and, unlike Flannel, enforced `NetworkPolicy`.

## Why it is still mapped here

Plenty of existing clusters run it, so it shows up as the **starting point of a migration**
rather than a destination. Moving off it means replacing the CNI, which is not an in-place
operation — see [../README.md](../README.md#5-anti-patterns).

## What to use instead

| Coming from Weave for… | Go to |
|---|---|
| simple overlay, no policy needed | [Flannel](../flannel/) |
| overlay plus NetworkPolicy | [Calico](../calico/) |
| policy, observability, kube-proxy replacement | [Cilium](../cilium/) |

---

[← CNI](../README.md)
