[← Chaos engineering](../README.md)

# LitmusChaos

<https://github.com/litmuschaos/litmus>
<https://github.com/litmuschaos/litmus-helm>
<https://github.com/litmuschaos/chaos-charts>
<https://litmuschaos.github.io/litmus/experiments/categories/contents/>

---

## The problem it solves

Chaos engineering as a **platform** rather than a fault injector: experiments defined as CRDs,
a hub of prebuilt ones, workflows that chain them, scheduling, and a UI that records results
over time.

That last part is what makes it a platform. An experiment run once and forgotten teaches
little; a scheduled experiment whose result is tracked is a regression test for resilience.

| Concept | What it is |
|---|---|
| `ChaosExperiment` | the fault definition — pod delete, network loss, CPU hog |
| `ChaosEngine` | binds an experiment to a target workload |
| `ChaosResult` | the outcome, including whether the hypothesis held |
| Chaos Hub | a catalogue of ready experiments |

## When to use it

- you want a **catalogue** rather than writing fault injection from scratch
- experiments should be scheduled and their results tracked
- non-engineers need to see what was tested and what happened

## When not to use it

- you want the broadest fault types, especially kernel, IO and time — [Chaos Mesh](../chaos-mesh/README.md) goes further
- the requirement is continuous random pod termination — [chaoskube](../chaoskube/README.md) is a fraction of the footprint
- there is no observability yet, in which case none of this produces learning

## The `ChaosResult` is the point

Most chaos tools inject a fault and leave interpretation to you. Litmus models the **probe** —
a check that defines whether the steady state held — so the experiment produces a pass or fail
rather than a shrug.

That is what turns it from an event into a test, and it is the main reason to choose the
platform over a simpler tool.

---

[← Chaos engineering](../README.md)
