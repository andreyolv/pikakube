[← Peer-to-peer image distribution](../README.md)

# Dragonfly

<https://github.com/dragonflyoss/Dragonfly2>
<https://github.com/dragonflyoss/helm-charts>

---

## The problem it solves

**Peer-to-peer distribution of large files, of which container images are one case.** Dragonfly
started at Alibaba, is a CNCF project, and is the most capable — and heaviest — option in
[`p2p-mirror/`](../README.md).

The architecture is a real distributed system rather than a `DaemonSet`:

| Component | Role |
|---|---|
| **Manager** | configuration, cluster membership, a web UI, and a database behind it |
| **Scheduler** | decides which peers a given peer should download from |
| **Seed peer** | a persistent peer that fetches from the origin and holds content deliberately |
| **Peer (dfdaemon)** | on every node; serves as the registry mirror and participates in the swarm |

What that buys over the stateless approach:

| Capability | Detail |
|---|---|
| **Seeding** | content can be fetched to seed peers **before** anyone needs it — the cold-start case Spegel cannot cover |
| Not only images | any file over HTTP: model weights, datasets, binaries, package archives |
| Scheduling policy | the scheduler optimises peer selection rather than relying on discovery alone |
| Piece-level transfer | files are split into pieces, so partial content is shareable |
| Observability | a manager UI, metrics, and a view of the swarm |
| Preheating | an API to warm the cluster ahead of a rollout |

**Preheating is the distinguishing feature.** Before a large rollout, content is pushed into seed
peers, so the first node to need it already has a local source. That directly addresses the
limitation in [Spegel](../spegel/README.md), where the first pull always goes upstream.

## When to use it

- **very large clusters** — hundreds of nodes, where registry fan-out dominates rollout time
- **very large images**: ML and CUDA base images, JVM monoliths, anything measured in gigabytes
- when **non-image files** also need distributing — model weights are the common case, and nothing
  else here does it
- when the **first** pull matters and content must be seeded ahead of a rollout
- edge or bandwidth-constrained sites where each location should fetch from the origin once

## When not to use it

- **small and medium clusters** — a manager, a scheduler, seed peers, a database and a per-node
  daemon is a large amount of infrastructure for a problem
  [`../../cache/`](../../cache/README.md) solves
- as a first experiment with P2P: [Spegel](../spegel/README.md) tests the idea with a fraction of
  the commitment
- where there is no appetite to operate another control plane, in the path of every image pull
- where node-level container runtime configuration cannot be managed

## Notes

Recorded links:

- <https://github.com/dragonflyoss/Dragonfly2> — the project. Dragonfly2 is the rewrite; the
  original Dragonfly is superseded, and the `2` in the repository name is the version that
  matters.
- <https://github.com/dragonflyoss/helm-charts> — the official chart repository, used here.

Recorded operational notes:

```bash
k port-forward svc/dragonfly-manager 8080
```

The manager's web UI. This is the console for the whole system — cluster membership, scheduler
configuration, seed peer status, preheat jobs. It is also the difference from
[Spegel](../spegel/README.md) in one observation: there is something to look at, because there is
state to look at.

> create account

The manager requires an account before the UI is usable, so first contact is a sign-up rather than
a login. Worth recording because it is a small surprise, and worth taking as a reminder: the
manager is an authenticated control plane holding cluster configuration, and it must not be
exposed beyond a `port-forward` without thought.

What is configured here: a Flux `HelmRelease` at chart version **1.3.17**, in its own namespace,
with values left as comments pointing at the chart's `values.yaml`. The chart deploys the whole
component set, and the two things to size before it is anything other than a trial are the
manager's database and the seed peers' storage — the seed peers hold real content, so their disks
must be planned rather than defaulted.

As with every tool in this folder, containerd must be configured to use the local peer as a
registry mirror. That configuration is on the node, not in the chart, and a node pool created
without it silently bypasses Dragonfly entirely.

## Where it fits here

The heavyweight option in [`p2p-mirror/`](../README.md), and the only one that can **seed**.

The sequence that makes sense: start with [`../../cache/`](../../cache/README.md), try
[Spegel](../spegel/README.md) when the cluster is large enough to justify P2P at all, and move to
Dragonfly when either the first pull of a new image is itself the problem, or non-image artefacts
need the same treatment. [Kraken](../kraken/README.md) is reference material rather than a third
choice.

By the threshold in [§2 of the parent](../README.md#2-where-the-threshold-is), none of this is
warranted at this cluster's size.

---

[← Peer-to-peer image distribution](../README.md)
