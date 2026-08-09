[← CI/CD](../README.md)

# Argo Workflows

<https://github.com/argoproj/argo-workflows>
<https://github.com/argoproj/argo-helm>
<https://argo-workflows.readthedocs.io/en/latest/security/>
<https://github.com/argoproj/argo-workflows/tree/main/examples>

---

## The problem it solves

Kubernetes runs containers. It has no way to say *"run this container, then those three in
parallel, then this one only if all of them succeeded, passing an artifact along the way."* A
`Job` runs one thing. Chaining `Job`s by hand means writing a controller.

Argo Workflows is that controller. A `Workflow` is a **DAG or a sequence of steps, where every
step is a container**, with parameters, artifacts, conditionals, loops (`withItems`), retries,
timeouts and fan-out/fan-in. It is implemented as CRDs, so a pipeline is a Kubernetes object —
reconciled, RBAC-controlled, and visible to `kubectl` like anything else.

**It is a general workflow engine, not a CI tool.** CI is one thing you can express in it. So is
ETL, batch ML training, data processing, and any pipeline whose steps happen to be containers.
Filing it under `cicd/` is a convenience, and the boundary against
[`data-engineering/orchestration/`](../../../data-engineering/orchestration/README.md) is set out
in [CI/CD §7](../README.md#7-boundary-argo-workflows-is-not-only-ci): **Argo Workflows is
container-native DAGs on Kubernetes; Airflow is a data-pipeline scheduler.**

## When to use it

- A pipeline of **heterogeneous containers** — different languages, different images, no shared
  runtime — that must run in a specific order on Kubernetes
- **Massive parallelism**: fan out to hundreds of pods, wait for all of them, fan back in. This is
  what it is genuinely good at, and few alternatives do it as cheaply
- Batch and scientific workloads — simulations, rendering, genomics, model training — where the
  unit of work is a container and the scheduler is Kubernetes
- CI **inside the cluster**, when builds must run where the cluster is and a self-hosted GitHub
  runner is not the right shape
- Event-driven pipelines, combined with **Argo Events** (in `infrastructure/devops/event-driven/`)
  for triggers, and `CronWorkflow` for schedules
- You already run Kubernetes and do not want a second scheduler with its own worker fleet

## When not to use it

- It is a **data pipeline** needing backfill, catchup, connections, sensors, or dataset lineage.
  Argo has no notion of any of those — use
  [Airflow](../../../data-engineering/orchestration/airflow/README.md) or a peer
- You want **pipeline-as-code**. Workflows are YAML, and complex ones are large YAML. The Python
  SDK (Hera) helps; it is still generating YAML underneath. [Dagger](../dagger/README.md) is the
  answer if escaping YAML is the goal
- The pipeline is standard CI on GitHub. [GitHub Actions](../github-actions/README.md) with
  self-hosted runners gives you the ecosystem, the UI and the PR integration for far less
- You do not run Kubernetes. There is no other mode
- You need a polished multi-tenant UI with fine-grained access control out of the box. The auth
  story is workable, not pleasant — see the notes
- Short, latency-sensitive tasks. Every step is a pod, and pod start-up dominates anything that
  takes seconds

## Notes

**The two upstream repositories** are split, as usual for Argo projects:
<https://github.com/argoproj/argo-workflows> for the controller and CRDs,
<https://github.com/argoproj/argo-helm> for the charts (shared with Argo CD, Rollouts and Events).
Chart version and application version are different numbers — the `0.45.2` deployed here is the
chart.

**<https://argo-workflows.readthedocs.io/en/latest/security/>** — the security documentation, and
the reason `secure: true` is set in the HelmRelease. That page is the one to read before exposing
anything: it covers the server authentication modes (`server`, `client`, `sso`), the fact that
workflow pods run with a ServiceAccount that determines what the workflow can do to the cluster,
and the artifact-repository access model. **A workflow is arbitrary container execution with a
ServiceAccount attached** — whoever can submit one has whatever that ServiceAccount has.

**Authentication is the recorded sore point.** Getting a token for the UI means creating a
ServiceAccount, a Role, a RoleBinding and a ServiceAccount token Secret by hand, then extracting
it:

```
ARGO_TOKEN="Bearer $(kubectl get secret argo-workflow-ui-service-account-token -o=jsonpath='{.data.token}' | base64 --decode)"
echo $ARGO_TOKEN
```

The recorded verdict on this is blunt: **"pretty crap, isn't it"**, with
<https://github.com/argoproj/argo-workflows/discussions/13257> as the reference. The complaint is
fair and worth understanding rather than just noting. Argo Workflows has no user database. In
`client` auth mode the UI expects you to paste a Kubernetes bearer token, so "logging in" means
manufacturing a ServiceAccount token out of band and pasting a base64-decoded blob into a browser.
Since Kubernetes 1.24, ServiceAccounts no longer auto-create token Secrets, so even that Secret
has to be declared explicitly — which is exactly what `rbac.yaml` here does, with the
`kubernetes.io/service-account.name` annotation.

The consequence: **for anything with more than one user, SSO mode is the only sane option**, and
the manual-token path is a bootstrap mechanism rather than a way to run the UI. That is the real
content of the complaint.

**<https://github.com/argoproj/argo-workflows/tree/main/examples>** — the upstream examples
directory, and the fastest way to learn what the DAG syntax can express. Worth going through
before writing a workflow from scratch; most non-obvious features (artifact passing, `withItems`,
conditional `when`, exit handlers, suspend/resume) are demonstrated there.

**What is deployed here:**

| Piece | Detail |
|---|---|
| Chart | HelmRelease `argo-workflows` `0.45.2`, from the `argo` HelmRepository |
| `secure: true` | TLS on the server, per the security documentation above |
| `crds.keep: false` | **CRDs are deleted when the release is removed** — and every `Workflow` object with them |
| `rbac.yaml` | a hand-written `argo-workflow-ui` ServiceAccount, a **read-only** Role, a RoleBinding, and a long-lived token Secret |

Two of those deserve attention.

**`crds.keep: false` is a deliberate but sharp choice.** The Helm default is to keep CRDs on
uninstall, precisely so that removing the release does not destroy the resources. Setting it to
`false` makes uninstall clean and complete — appropriate for a mapped, experimental install, and
dangerous if real workflow history ever matters.

**The RBAC role is genuinely read-only**, and it is worth noting what that means for the UI: `get`,
`list`, `watch` on pods, pod logs and events, plus the `argoproj.io` resources
(`workflows`, `workflowtemplates`, `clusterworkflowtemplates`, `cronworkflows`,
`workfloweventbindings`, `workflowtaskresults`, and Argo Events' `eventsources` and `sensors`).
No `create`, so **this token cannot submit a workflow** — it can only observe. That is the correct
default for a UI token, and it means submission needs a separate, more privileged identity. The
role is modelled on upstream's `workflow-aggregate-roles.yaml`, which is linked in the file itself.

One cosmetic defect in `rbac.yaml`: `cronworkflows` is listed **twice** in the resources list.
Harmless — Kubernetes deduplicates — but it is a copy-paste artefact.

**The example** in `example/workflow.yaml` is upstream's diamond DAG: four nodes `A → (B, C) → D`,
where each node is itself a `withItems` fan-out of three parallel `echo` steps. Twelve pods from
about forty lines of YAML. It demonstrates the two composition mechanisms together — `dag` with
`depends: "B && C"` for the graph, `steps` with `withItems` for the fan-out — which is exactly what
Argo is good at and what a `Job` cannot express.

---

[← CI/CD](../README.md)
