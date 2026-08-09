[← Manifest templating](../README.md)

# Helmfile

<https://github.com/helmfile/helmfile>

---

## The problem it solves

One Helm release is a command. Thirty Helm releases is a shell script that nobody trusts —
repositories to add, values files to pass, ordering between them, and a different set of
overrides per environment.

Helmfile makes that set **declarative**. A `helmfile.yaml` lists the releases, their charts,
versions, namespaces, values and dependencies, and `helmfile apply` reconciles the lot. It also
gives you `helmfile diff`, which shows what an apply would change before it changes it.

## When to use it

- **Many Helm releases and no GitOps controller.** This is the real case: a cluster driven from
  CI or a workstation, where the alternative is a `Makefile` wrapping `helm upgrade --install`.
- **Bootstrapping.** The controller itself, and whatever it needs to exist before it can start
  reconciling, has to be installed by something outside the controller.
- **Local and ephemeral clusters** — a kind or minikube environment stood up and torn down, where
  running a reconciler is more machinery than the task deserves.

## When not to use it

- **When Flux or Argo CD is already in the cluster.** Both reconcile Helm releases from Git
  continuously; Helmfile does the same thing on demand, from wherever it happens to run. Having
  both means two systems believe they own the release.
- **For a handful of releases.** The abstraction costs more than it saves below roughly a
  dozen.

## Notes

The recorded link is [helmfile/helmfile](https://github.com/helmfile/helmfile).

**The honest position: Helmfile has been largely superseded by GitOps controllers.** It was
built for a world where the sequence "add repositories, template values, upgrade in order" was
something a human or a CI job ran. Flux's `HelmRelease` and Argo CD's Helm support now do that
continuously, inside the cluster, with drift detection and a reconciliation loop — which is
strictly more than a command you have to remember to run.

What survives is the bootstrap gap. Something has to install the controller, and that something
cannot be the controller. Helmfile is a reasonable answer there, and so is a shell script.

For this repository the point is moot: Flux owns every Helm release
([`platform-engineering/gitops/`](../../../platform-engineering/gitops/README.md)), so Helmfile
is recorded as an alternative that has been evaluated, not as a tool in use.

---

[← Manifest templating](../README.md)
