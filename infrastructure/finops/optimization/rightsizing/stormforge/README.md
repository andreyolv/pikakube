[← Right-sizing](../README.md)

# StormForge

<https://github.com/thestormforge/helm-charts>

---

## The problem it solves

The open-source right-sizing tools give you a number and stop. Someone has to decide how much margin
to add, whether this workload can tolerate being wrong, and then repeat that judgement across every
workload, every month, forever. That is the part that does not happen.

StormForge is a **commercial SaaS** (Optimize Live) that takes the whole loop: an agent in the
cluster reports usage to the vendor's control plane, machine-learned models produce recommendations
for **both requests and limits**, and the recommendations can be applied automatically on a schedule
rather than sitting in a report.

Two things distinguish it from VPA-derived tooling:

- **it recommends limits as well as requests**, which most tools treat as an afterthought despite
  limits being what decides whether a container is throttled or OOM-killed
- **recommendations are tuned against a stated reliability target**, not a raw percentile. You say
  how much headroom the workload should keep; the model works backwards from that. That framing is
  what makes the output arguable with application teams, which is the real bottleneck

It is also designed to coexist with the HorizontalPodAutoscaler, which is the collision that stops
most VPA deployments — see [`rightsizing/`](../README.md) section 5.

## When to use it

- many clusters and many workloads, where the recurring judgement will not be made by hand
- when the right-sizing conversation keeps stalling on "how much headroom is safe" and a target-based
  answer would unblock it
- workloads already running an HPA, where VPA in `Auto` mode is not an option
- when the demonstrated saving comfortably exceeds the licence and the alternative is that nothing
  changes

## When not to use it

- before establishing the gap for free. [KRR](../krr/README.md) needs no install and
  [Goldilocks](../goldilocks/README.md) needs no vendor; if the answer is "requests are broadly
  sane", none of this is worth buying
- when workload telemetry leaving the cluster for a vendor's control plane is not acceptable
- when the blocker is teams merging changes rather than producing recommendations — no vendor solves
  that
- as a cost visibility tool; that is [`visibility/`](../../../visibility/README.md)
- alongside VPA in `Auto` mode on the same workloads — two controllers mutating the same resources

## Notes

Original notes recorded for this folder, translated and explained.

**<https://github.com/thestormforge/helm-charts>** — the vendor's public chart repository. The
charts are open; the product they connect to is not. Note that the deployment here does not use this
Git repository directly — it pulls the chart as an OCI artefact from
`registry.stormforge.io`, which is the current distribution route.

**On the deployment here.** Flux, from an `OCIRepository` at
`oci://registry.stormforge.io/library/stormforge-agent`, tag **2.3.0**, into a dedicated
`stormforge-system` namespace.

```yaml
clusterName: k8s-platform
stormforge:
  address: https://api.stormforge.io/
authorization:
  issuer: https://api.stormforge.io/
  clientID: xxxxxxxxxxx
  clientSecret: xxxxxxxxxxxxx
```

Points worth noting:

- **`clusterName` is the identity the vendor's console groups everything by.** It has to be unique
  and stable across clusters, and renaming it later orphans the history — the same discipline the
  cost tools in [`visibility/kubernetes/`](../../../visibility/kubernetes/README.md) apply with their
  cluster IDs.
- **The agent talks outbound to `api.stormforge.io`.** Workload telemetry leaves the cluster, and the
  recommendations come back from outside. That is the architectural fact to weigh, and it applies
  equally to [PerfectScale](../perfectscale/README.md), [CAST AI](../../node/castai/README.md) and
  [Spot Ocean](../../node/spot-ocean/README.md).
- **`clientID` and `clientSecret` are placeholders**, and are OAuth client credentials rather than a
  simple API token. They belong in a Secret referenced by `valuesFrom`, in the shape the
  [Kubecost](../../../visibility/kubernetes/kubecost/README.md) release in this repository already
  uses — not in a values file in Git.
- **Pinned by tag rather than digest.** OCI sources support digest pinning, which is one of the
  reasons to prefer them; a tag can be moved underneath you.

**What is not recorded here** is the decision that matters most: whether the agent is permitted to
**apply** recommendations or only to produce them. That is the same recommend-versus-enforce split as
[VPA](../vpa/README.md), with the additional wrinkle that the deciding party is outside the cluster
and outside Git. If it applies changes, the manifests in this repository and the running pods will
disagree, permanently — decide that deliberately rather than discovering it.

---

[← Right-sizing](../README.md)
