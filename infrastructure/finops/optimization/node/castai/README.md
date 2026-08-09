[← Node optimization](../README.md)

# CAST AI

<https://github.com/castai/helm-charts>

Deployment shape: [`castai-agent-chart/`](castai-agent-chart/README.md)

---

## The problem it solves

Karpenter and the cluster-autoscaler give you the mechanism; somebody still has to own the policy —
which instance families are acceptable, how aggressive consolidation should be, which workloads may
run on spot, and what the requests should have been in the first place. On most platforms nobody
owns that, so it is tuned once and then decays.

CAST AI is a **commercial SaaS platform** that takes the whole loop: an agent in the cluster reports
workloads and capacity, the vendor's control plane decides, and — once you let it — it provisions
nodes, moves workloads onto cheaper and spot capacity, bin-packs the cluster and recommends or
applies right-sized requests. Cost reporting sits on top of the same data.

The property that makes it easy to evaluate: **the agent starts read-only.** Install it, wait, and
you get a costed report of what the cluster spends and what it estimates it could save — with no
authority to change anything. That is a genuinely low-commitment way to get a second opinion on
your own numbers.

## When to use it

- **nobody will own the tuning.** This is the honest reason to buy any tool in this category, and
  it is a legitimate one
- multiple clusters across multiple clouds, wanting one optimisation policy and one report
- as a **read-only benchmark**: run the agent for a month and compare its estimate against what
  the platform team believes
- when the savings clearly exceed the fee and the alternative is that nothing happens at all

## When not to use it

- when [Karpenter](../karpenter/README.md) plus a week of work reaches the same place — after the
  first year, that week is much cheaper than a recurring share of savings
- when an external control plane holding authority to delete production nodes is unacceptable —
  which is a real position, not a paranoid one
- without answering what happens when the vendor's control plane is unreachable
- before right-sizing, or before PodDisruptionBudgets exist: automated bin-packing on a cluster
  whose requests are wrong evicts exactly the workloads that were surviving on slack
- purely for cost visibility, where [OpenCost](../../../visibility/kubernetes/opencost/README.md) is
  open source and answers the same question

## Notes

Original notes recorded for this folder, translated and explained.

**<https://github.com/castai/helm-charts>** — the vendor's chart repository. `castai-agent` is the
entry point: the read-only component that registers the cluster and reports inventory and cost. The
components that actually change things — the cluster controller, the evictor, the spot handler — are
separate charts installed afterwards, once you decide to grant that authority. The staging is
deliberate and is the reason evaluation is cheap.

**The alternative install path.**

```bash
curl -H "Authorization: Token XXXXXXXXXXXXXXXXX" \
  "https://api.cast.ai/v1/agent.yaml?provider=aks" \
  | kubectl apply --dry-run=client -f - -o yaml > castai.yaml
```

What this does: CAST AI's API **generates the agent manifests for your cloud and your account** —
`provider=aks` here — already carrying the cluster's credentials. The usual instruction is to pipe
that straight into `kubectl apply`, which means applying manifests nobody has read.

The `--dry-run=client -f - -o yaml > castai.yaml` part is the improvement, and it is a pattern worth
stealing generally: **render the manifests to a file instead of applying them.** `--dry-run=client`
validates locally without touching the cluster, `-o yaml` prints the normalised objects, and the
redirect captures them. The result is a file you can read, diff, and commit to Git so Flux owns it —
turning a `curl | kubectl apply` install into a reviewed, reconciled one.

One caution that follows directly: the generated file **contains the API token**. It cannot be
committed as-is; the secret has to be extracted and handled the way every other secret on this
platform is.

**On the deployment here.** Flux, from `https://castai.github.io/helm-charts`, chart `castai-agent`
into a dedicated `castai-agent` namespace, with `provider: aks`, `createNamespace: false` — the
namespace is a separate manifest, which is the correct split when Flux owns the lifecycle — and
`apiKeySecretRef` left empty, so the credential is expected to come from a Secret rather than the
values file.

No chart version is pinned. See [`castai-agent-chart/`](castai-agent-chart/README.md).

---

[← Node optimization](../README.md)
