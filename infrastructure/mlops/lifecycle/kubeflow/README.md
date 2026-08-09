[← Lifecycle](../README.md)

# Kubeflow

<https://github.com/kubeflow/kubeflow>
<https://github.com/kubeflow/manifests>
<https://github.com/kubeflow/training-operator>

---

## The problem it solves

Kubeflow is a **full ML platform on Kubernetes**, not a tool. It bundles the pieces a team would
otherwise assemble themselves:

| Component | What it does |
|---|---|
| **Pipelines** | authoring, running and versioning multi-step ML workflows as containers, with a UI and run history |
| **Notebooks** | on-demand Jupyter servers per user, with quotas, images and volumes managed by the platform |
| **Training operators** | CRDs for distributed training — `PyTorchJob`, `TFJob`, `XGBoostJob` — so multi-node training is a Kubernetes object |
| **Katib** | hyperparameter search and neural architecture search as a controller |
| **KServe** | model serving via an `InferenceService` CRD, with autoscaling and canaries |
| **Central dashboard + profiles** | multi-tenancy: per-user namespaces, isolation and RBAC |

The problem it genuinely solves is **multi-tenancy over shared, expensive compute**. Several teams
want GPUs, isolated namespaces, self-service notebooks and reproducible pipeline runs, and nobody
wants to build that. Kubeflow is that, off the shelf.

It is powerful and it is genuinely heavy. Both halves are true, and the second half is the one
that gets underweighted — see [`../README.md`](../README.md#3-mlflow-vs-kubeflow) for the
comparison with MLflow.

## When to use it

- **Several teams share GPU capacity** and isolation between them is a requirement rather than a
  preference.
- Pipelines must be authored by data scientists who will not write Kubernetes YAML, and pipeline
  run history is something people actually look at.
- Distributed training is normal work, not an occasional experiment — the training operators are
  the strongest single component and the reason to look at Kubeflow at all.
- Self-service notebooks are a request you keep receiving and keep handling manually.
- There is a person or a team whose job includes operating this. That is the real entry
  requirement.

**Take the components separately first.** `training-operator`, Kubeflow Pipelines and KServe all
install and run on their own, alongside MLflow, without the dashboard, profiles or the rest of the
platform. That is usually the better trade: you get the piece that was actually needed without
adopting the operational surface of the whole thing.

## When not to use it

- **You have a handful of models and one team.** This is the common case and the common mistake.
  What follows adoption is that you operate an ML platform in order to run three models —
  upgrades, component drift, auth integration, storage, GPU scheduling — instead of shipping
  models. [MLflow](../mlflow2/README.md) covers tracking and the registry for one container and a
  database.
- You only need experiment tracking. Kubeflow is not a tracking server, and reaching for it to get
  one is enormously disproportionate.
- Nobody owns the platform. An unowned Kubeflow install drifts, then breaks on the next Kubernetes
  upgrade, then gets abandoned with models inside it.
- The install path is a problem for you — see the notes.

## Notes

**"Deploy by kustomization very bad"**

The original note. Kubeflow's supported installation is `kubeflow/manifests`, a large Kustomize
tree applied with `kustomize build | kubectl apply`. The complaint is well founded:

| Consequence | Why it hurts |
|---|---|
| No values file | configuration means patching overlays, so every choice is a fork of upstream |
| No release lifecycle | there is no `helm upgrade`; upgrading is diffing two manifest trees and reconciling by hand |
| No install/uninstall boundary | nothing tracks what a release owns, so removal is manual and leaves residue |
| Apply ordering matters | CRDs, webhooks and components must land in an order the tool does not enforce; the documented workaround is to re-run the apply until it converges |
| Poor GitOps fit | rendering a huge tree into a repository is possible, but every upstream bump re-renders everything and the diff is unreadable |

The practical effect: the install is a one-way door. It works when it works, and there is no
supported path back or forward.

**"Waiting for a Helm chart release" — <https://github.com/kubeflow/manifests/issues/2730>**

The upstream issue tracking an official Helm chart for the Kubeflow manifests. This is the reason
Kubeflow is **documented here and not deployed**: the decision was made to wait for a packaged
install rather than take on a hand-maintained Kustomize tree.

That is a defensible position and worth stating as a position rather than as an absence. The
alternatives, if the wait becomes indefinite:

- **Take the components individually.** `training-operator` and KServe both ship their own
  installs and do not require the platform. This gets most of the value for a fraction of the
  surface.
- **Use a packaged distribution.** Deployment Kubeflow (deployKF), Charmed Kubeflow and the
  vendor distributions exist precisely because upstream's install is what it is. Each adds a
  dependency on that distributor.

**Note that the same complaint appears in [`../mlflow/`](../mlflow/README.md)** — "still no Helm
chart, unbelievable". Two of the three tools in this folder are held back by packaging rather than
by capability, which is a real and unglamorous constraint on what gets adopted here.

**Related component links recorded in [`../../README.md`](../../README.md#7-notes):**
`kubeflow/training-operator` for distributed training CRDs, and `kserve/kserve` for serving —
both usable without the rest of Kubeflow.

---

[← Lifecycle](../README.md)
