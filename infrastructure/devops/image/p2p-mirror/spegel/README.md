[← Peer-to-peer image distribution](../README.md)

# Spegel

<https://github.com/spegel-org/spegel>

---

## The problem it solves

**Stateless peer-to-peer image distribution.** Spegel runs as a `DaemonSet`, reads what containerd
has **already stored** on each node, advertises those layers to a peer network, and serves them to
other nodes over HTTP.

The word that matters is *stateless*. Spegel stores nothing of its own — no registry, no database,
no seeded content, no volumes. It is a view over the content store that already exists on every
node, which produces properties nothing else in this folder has:

| Property | Consequence |
|---|---|
| **No storage of its own** | nothing to back up, nothing to size, nothing to fill |
| **No control plane** | no manager, no scheduler, no database to operate |
| Peer discovery via libp2p | nodes find each other; a bootstrap peer is all that is configured |
| Removal is clean | delete the `DaemonSet` and the cluster is exactly as before |
| Failure is soft | if no peer has the layer, the pull falls back to the upstream registry |

The limitation is the same design, seen from the other side: **Spegel can only serve what a node
has already pulled.** The first pull of a new image goes to the registry, and a cold cluster gets
no benefit at all. It flattens the fan-out; it does not eliminate the first fetch.

It works by registering as a registry **mirror** in containerd's configuration, so pulls are
directed at the local Spegel instance first. That configuration lives on the node, not in a
manifest — the part of adoption that is more than a `helm install`.

## When to use it

- **the first P2P tool to try**, because the cost of trying it is close to zero
- large clusters where the same images are pulled by many nodes — the case in
  [§2 of the parent](../README.md#2-where-the-threshold-is)
- rolling updates of a `DaemonSet` or a large `Deployment`, where the fan-out is simultaneous
- autoscaled or spot node pools, where nodes join constantly and pull the same set of images
- reducing registry egress cost where it is billed per gigabyte

## When not to use it

- **small clusters** — a `DaemonSet` in the pull path solving a problem that does not exist
- when the **first** pull of a new image is the thing that hurts; Spegel cannot seed content, and
  pre-pulling ([`../../cache/`](../../cache/README.md)) or Dragonfly is the answer
- with a container runtime other than containerd, or where node-level runtime configuration cannot
  be managed
- as a substitute for a registry: it is a distribution accelerator, and pulls still resolve
  upstream when no peer has the content

## Notes

Recorded link:

- <https://github.com/spegel-org/spegel> — the project. It has its own GitHub organisation, is
  actively developed, and is by a wide margin the newest and most actively maintained of the three
  tools in [`p2p-mirror/`](../README.md).

What is configured here: a Flux `HelmRelease` at chart version **v0.0.28** from the project's chart
repository, in its own namespace, with values left as comments pointing at the chart's
`values.yaml`.

The `v0.0.x` chart version is worth reading as the signal it is: Spegel is young. That is the
counterweight to everything good about its design — it is the cleanest architecture in this
folder and the least battle-tested. Pin the version, and read the release notes before upgrading
something that sits in the path of every image pull.

**The prerequisite that is easy to miss**: containerd must be configured to use Spegel as a
registry mirror, via `hosts.toml` entries under `/etc/containerd/certs.d/`. Some distributions
allow the chart to write that configuration; others do not. Two consequences follow. Nodes that
join a cluster without that configuration **silently bypass Spegel** — pulls simply go upstream
and nothing reports an error, so the benefit quietly disappears on a new node pool. And the
configuration must be part of the node bootstrap, not a one-off applied by hand.

Also worth knowing: containerd's discard-unpacked-layers optimisation removes the compressed layer
blobs after unpacking, and Spegel serves compressed layers. Where that setting is enabled, a node
has the image and cannot share it. It is a known interaction, documented upstream, and exactly the
kind of thing to verify with a test pull rather than assume.

## Where it fits here

**The one to reach for first** among the three in [`p2p-mirror/`](../README.md), for a reason that
is architectural rather than a preference: it adds no state, no control plane and no new failure
domain, and it can be removed as cleanly as it was added.

[Dragonfly](../dragonfly/README.md) is the heavier, more capable option — it can seed content
deliberately and handles arbitrary files, at the cost of a manager, a scheduler and a database.
[Kraken](../kraken/README.md) is reference material.

By the threshold in [§2 of the parent](../README.md#2-where-the-threshold-is), none of this is
warranted at this cluster's size. Spegel is what to deploy when it is.

---

[← Peer-to-peer image distribution](../README.md)
