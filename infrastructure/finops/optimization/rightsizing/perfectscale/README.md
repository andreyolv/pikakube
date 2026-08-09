[← Right-sizing](../README.md)

# PerfectScale

<https://github.com/perfectscale-io/perfectscale-io.github.io>

---

## The problem it solves

Right-sizing is usually framed as a cost exercise, which is why application teams resist it: the
person asked to lower a request carries all of the risk and none of the saving.

PerfectScale is a **commercial SaaS** that frames the same work as a **reliability and cost
trade-off** in both directions. An agent reports workload and cluster telemetry; the platform
identifies workloads that are over-provisioned *and* workloads that are under-provisioned — the ones
being throttled, OOM-killed or evicted — and recommends requests and limits with the effect on both
axes stated.

That framing is the differentiator. "This workload has been OOM-killed four times this month and is
under-requested" is a conversation application teams engage with; "this workload could be 30%
cheaper" is one they defer. It also covers multiple clusters in one place, with the change
attributed over time.

Closed source. Priced per node or per cluster on a subscription.

## When to use it

- an estate of several clusters where nobody will own the recurring right-sizing loop
- when the argument needs to include reliability, not only cost — under-provisioning is a real and
  usually unmeasured problem
- when a cost-and-reliability report for management is part of what is being bought
- when it has been benchmarked against a free run of [KRR](../krr/README.md) and demonstrably says
  something more

## When not to use it

- before running [KRR](../krr/README.md), which is free and answers the sizing question directly
- when [Goldilocks](../goldilocks/README.md) plus a review cadence would close the gap — the
  expensive part of right-sizing is teams merging changes, and no vendor solves that
- when workload telemetry may not leave the cluster
- as a cost allocation tool — that is [`visibility/kubernetes/`](../../../visibility/kubernetes/README.md),
  and [OpenCost](../../../visibility/kubernetes/opencost/README.md) is free
- alongside another mutating right-sizer on the same workloads

## Notes

Original notes recorded for this folder, translated and explained.

**<https://github.com/perfectscale-io/perfectscale-io.github.io>** — note carefully what this
repository actually is: **the documentation site**, not the product. That is the whole signal. The
organisation publishes docs on GitHub and nothing else, so there is no source to read, no chart to
inspect before installing, and no way to evaluate the recommendation logic other than by running the
agent and trusting the output.

Compare with the rest of this folder: [VPA](../vpa/README.md)'s algorithm is at least readable in
source even though it is undocumented, and [KRR](../krr/README.md)'s strategy is a few files. Here
the model is a black box by construction. That is not a reason to reject it — most SaaS is — but it
does mean the only meaningful evaluation is empirical: run it beside a free tool and compare what
each says about workloads you already understand.

**Nothing is deployed for this in the repository.** It is mapped as an evaluated option alongside
[StormForge](../stormforge/README.md), which occupies the same commercial slot and *is* deployed.
Both put an agent in the cluster and a control plane outside it; choosing between them is a
procurement exercise, and the useful input is a side-by-side trial on the same cluster over the same
weeks.

---

[← Right-sizing](../README.md)
