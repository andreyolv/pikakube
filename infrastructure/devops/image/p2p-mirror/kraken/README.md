[← Peer-to-peer image distribution](../README.md)

# Kraken

<https://github.com/uber/kraken>

---

## The problem it solves

**A P2P-backed registry, built at Uber for very large clusters.** Kraken is not a mirror in front
of a registry; it is a registry whose distribution layer is a BitTorrent-derived peer network.

| Component | Role |
|---|---|
| **Agent** | on every node; serves the registry API locally and participates in the swarm |
| **Origin** | seeders backed by durable storage — the authoritative copies |
| **Tracker** | coordinates which peers hold which content |
| **Build index** | maps tags to digests, and handles replication between clusters |
| Proxy | the ingress point for pushes |

The published claim is distribution of terabytes per second across thousands of hosts, which is
the scale it was built for. Architecturally it is interesting: the origins are the durable layer
and the agents are ephemeral, so the swarm can be entirely rebuilt without losing content.

## When to use it

Realistically: **studying it.** The architecture is worth understanding — the separation of
origin, tracker and index is a clean way to think about P2P distribution, and it predates most of
the alternatives.

For actual deployment, the honest answer is that the reasons to choose it over
[Spegel](../spegel/README.md) or [Dragonfly](../dragonfly/README.md) have largely gone.

## When not to use it

- **as a new deployment** — see the maintenance note below
- where a supported, actively developed tool is required: Spegel and Dragonfly are both
  substantially more alive
- where a Helm chart from a chart repository is expected; there is none
- on small or medium clusters, where P2P is unwarranted at all —
  [§2 of the parent](../README.md#2-where-the-threshold-is)

## Notes

Recorded link:

- <https://github.com/uber/kraken> — the project.

**Maintenance status, stated plainly.** Kraken has been very quiet for years. Uber open-sourced it
and continued to use it internally, but public development slowed to occasional maintenance
commits, and the community around it is small. It is not formally archived; it is also not a
project to build a dependency on in 2026 without checking its current state first.

**A concrete symptom of that, visible in this repository.** The Flux `HelmRelease` here cannot use
a `HelmRepository`, because Kraken publishes no chart repository. It uses a `GitRepository` source
pointing at the `helm` directory inside `uber/kraken`:

```yaml
chart:
  spec:
    chart: helm
    sourceRef:
      kind: GitRepository
      name: kraken
```

That is a workable pattern and it is also a signal. A project that ships a chart directory in its
source tree and never publishes it is a project without a release process for its Kubernetes
distribution — so upgrades track a Git ref rather than a version, and there are no chart release
notes to read.

The values recorded here trim it to a minimal single-replica installation:

```yaml
tracker:     { replicas: 1 }
build_index: { replicas: 1 }
origin:      { replicas: 1 }
testfs:      { enabled: false }
```

One replica of each component is an evaluation configuration, not a deployment one — the origins
are the durable layer, so a single origin is a single point of failure for the content itself.
`testfs` is Kraken's built-in test filesystem backend, disabled here, which means a real storage
backend would have to be configured before the origins could hold anything.

## Where it fits here

Reference material in [`p2p-mirror/`](../README.md), and documented so the option is understood
rather than left as a name people half-remember.

For an actual deployment: **[Spegel](../spegel/README.md) first** — stateless, actively developed,
nearly free to try — and **[Dragonfly](../dragonfly/README.md)** when seeding or non-image
artefacts are needed. Kraken's contribution here is its architecture, not its availability.

---

[← Peer-to-peer image distribution](../README.md)
