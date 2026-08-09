[← Serverless](../README.md)

# Fission

<https://github.com/fission/fission>

---

## The problem it solves

A function platform for Kubernetes whose distinguishing feature is **how it answers the cold-start
problem**: instead of starting a pod when a request arrives, Fission keeps a pool of generic,
pre-warmed pods per *environment* (a language runtime) and injects the function's code into one of
them on demand.

That inverts the usual trade. Most platforms start cold and try to start faster; Fission pays for
idle capacity up front and gets a warm pod almost immediately.

The model in a handful of objects, which are the CRDs committed in `crds/` here:

| Resource | What it is |
|---|---|
| `Environment` | a language runtime, and the pool sizing that goes with it |
| `Package` | the source or the built artifact |
| `Function` | code plus the environment that runs it |
| `HTTPTrigger`, `TimeTrigger`, `MessageQueueTrigger`, `KubernetesWatchTrigger` | what invokes it |
| `CanaryConfig` | shifting a trigger's weight from an old function to a new one, in steps |

## When to use it

- **cold start is the constraint you actually care about**, and you will accept a permanently
  running pool to fix it
- many small handlers in the same few languages — the pool is shared, so a second function in an
  existing environment costs nothing extra
- you want triggers (HTTP, timer, message queue, Kubernetes watch) declared as resources rather
  than wired up by hand

## When not to use it

- you expected scale to zero to mean **zero cost** — the warm pool is the opposite of that
- a single function or a scheduled task: a `CronJob` does this without a control plane
- you install everything through Helm and want it to work on the first apply — see the CRD note
  below
- you want a worked Kubernetes example to copy from the project — there is not one, per the note
  below

## Notes

**Apply the CRDs before the HelmRelease.** This is the recorded finding, and it is the reason the
`crds/` folder exists in this directory at all. The command used to produce it:

```bash
kubectl create -k "github.com/fission/fission/crds/v1?ref=v1.20.5" --dry-run=client -o yaml \
  | kubectl-slice -f - -o ./crds
```

Reading it left to right: `kubectl create -k` renders the upstream kustomize directory for the
CRDs at a pinned tag, `--dry-run=client -o yaml` prints them instead of applying them, and
[`kubectl-slice`](https://github.com/patrickdappollonio/kubectl-slice) splits the resulting
multi-document stream into **one file per resource** — which is what produced the eight files
committed here. Those get applied first; the `HelmRelease` comes after.

Why this is necessary is not specific to Fission. **Helm does not reliably install a chart's CRDs
before the resources that depend on them** — the `crds/` directory of a chart is installed once
and never upgraded, and CRDs that live in `templates/` race the objects that use them. A single
`HelmRelease` therefore fails on first apply with `no matches for kind`, and succeeds on the
second reconcile, which is exactly the kind of intermittent behaviour that is miserable in a
GitOps loop. Splitting the CRDs out and applying them as a separate, ordered step is the general
workaround, and this repository hits the same problem with other operator charts. Treat it as a
Kubernetes and Helm limitation, not a bug in any one project.

**Version skew, worth noticing.** The command above pins the CRDs at `v1.20.5`; the `HelmRelease`
pins the `fission-all` chart at `1.20.4`. Close enough to work, and still a mismatch — the CRDs
and the controller that reconciles them should be bumped together, otherwise a field the new
controller expects may not exist in the committed schema.

**No examples for Kubernetes.** Recorded verbatim in the original note: the project does not offer
Kubernetes examples to copy from. Fission's documentation and tutorials are built around the
`fission` CLI — `fission env create`, `fission fn create` — rather than around the CRDs you would
actually commit to a GitOps repository. That gap is real work: adopting Fission here means
translating CLI tutorials into `Environment`, `Function` and `HTTPTrigger` manifests yourself,
using the committed CRD schemas as the reference. It is also why nothing beyond the CRDs and the
release exists in this folder.

**What is deployed here:** chart `fission-all` 1.20.4, from
`https://fission.github.io/fission-charts/`, in the `fission` namespace, with an empty `values`
block — so pool sizes, executor types and everything else are at their defaults.

---

[← Serverless](../README.md)
