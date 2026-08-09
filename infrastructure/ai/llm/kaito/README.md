[← LLM](../README.md)

# KAITO — Kubernetes AI Toolchain Operator

<https://github.com/kaito-project/kaito>

---

## The problem it solves

Deploying a model on Kubernetes by hand is a long list of decisions that have nothing to do with
the model: which GPU node type, whether nodes exist yet, how weights get onto the node, which
inference runtime, how to shard across GPUs, what the readiness probe should be, and how to
expose it.

KAITO turns that list into a **`Workspace` resource**. You declare the model — from a catalogue
of presets — and the hardware you want it on. The operator provisions the nodes if they are
missing, pulls the weights, picks and configures the inference runtime, and exposes an endpoint.

The part that distinguishes it from every other option in this folder is **node provisioning**.
vLLM and Ollama assume a GPU node is already there and scheduled. KAITO can create it. On a
cloud cluster with autoscaling that closes the last gap between "I want this model" and a
running endpoint.

The **preset** concept is the other half. A preset bundles a known model with a validated
runtime configuration, so the parallelism settings and resource requirements are the project's
problem rather than yours. That is a real reduction in work and a real constraint: you get the
models the catalogue covers, configured the way it configures them.

Its origin shows in the details. KAITO came out of Microsoft for AKS, and the assumptions that
travel with that are visible in this repository's own example — see the notes.

## When to use it

| Situation | Why KAITO |
|---|---|
| Model deployment should be declarative and reviewable | a `Workspace` in Git, reconciled like anything else |
| GPU nodes should appear on demand rather than sit idle | node provisioning is the differentiator |
| The models you want are in the preset catalogue | validated configuration you do not have to derive |
| Several teams deploy models and should not each learn GPU serving | the CRD is the interface |
| The cluster is on Azure/AKS | the path it is most tested on |

## When not to use it

| Situation | Use instead |
|---|---|
| One model, deployed once, tuned deliberately | [vLLM](../vllm/README.md) directly — an operator is overhead for a single workload |
| The model is not in the catalogue and the configuration is unusual | vLLM, where every knob is yours |
| Bare metal with a fixed GPU inventory | node provisioning is the main benefit and it does not apply |
| Local development | [Ollama](../ollama/README.md) |
| You want to control the runtime version independently | you inherit the operator's choices, which is the deal |

## Notes

The only thing recorded for KAITO in the original notes was the project URL:

- <https://github.com/kaito-project/kaito> — the project. Note the organisation is
  `kaito-project`, not `Azure` — it began as a Microsoft/AKS component and now develops under
  its own org, which is why it is worth evaluating on a non-Azure cluster at all.

**What is deployed here.** Flux tracks the project's Git repository at tag `v0.4.4`, with an
`ignore` block that excludes everything except `/charts/kaito`, and installs the `charts/kaito`
chart into the `kaito` namespace with empty values. Two things follow from that.

**The chart is installed from a `GitRepository`, not a Helm registry** — the only source of that
kind in this folder. The `ignore` block is what keeps Flux from cloning and watching the whole
project for a chart in one subdirectory; it is a small detail that matters for reconciliation
cost.

**The `values.yaml` comment in the `HelmRelease` points at
`charts/kaito/workspace/values.yaml`**, while the chart path installed is `charts/kaito`. Worth
verifying that the intended chart is being installed — KAITO's repository has historically
contained more than one chart, and the mismatch between the installed path and the documented
values file is the kind of thing that is invisible until an option silently does nothing.

**The example `Workspace` is Azure-specific.** It requests `phi-3.5-mini-instruct` as a preset,
on `instanceType: Standard_NC24ads_A100_v4` — an Azure VM SKU with an A100 — selected by the
label `apps: phi-3-5`. On any non-Azure cluster that instance type is meaningless and node
provisioning will not happen; the workspace would need a node that already carries the matching
label. This is the concrete form of the "it came from AKS" caveat above, and it is the first
thing to change if KAITO is evaluated here for real. It is also, usefully, a small preset: a
`mini` model is the right size for confirming the operator works before asking it for a GPU that
costs money.

---

[← LLM](../README.md)
