[← Flux](../README.md)

# Flux Operator

<https://github.com/controlplaneio-fluxcd/flux-operator>
<https://github.com/controlplaneio-fluxcd/charts>

---

## The problem it solves

`flux bootstrap` installs Flux by running a command. Everything Flux manages after that is
declarative; Flux itself is not. The controller versions in the cluster are whatever the CLI on
somebody's laptop produced, the component list was a flag, and cluster-specific adjustments —
node selectors, tolerations, resource limits — are kustomize patches maintained beside the
generated manifests.

Flux Operator replaces that with a **`FluxInstance` object**. Distribution version, registry,
component list, sync source, storage class and per-Deployment patches all become fields. Upgrading
Flux is editing `spec.distribution.version` and committing it. Adding a controller is adding a line.

The second thing it provides is the `FluxReport` — a single object summarising the health of the
whole installation: which controllers are running, at which versions, what the sync source is, and
what is failing. Without it, "is Flux itself healthy" is a question you answer by checking six
Deployments.

It is maintained by ControlPlane, not by the Flux project. That is worth knowing: it is a
well-regarded third-party operator around an upstream, with a commercial distribution behind it.

## When to use it

- the Flux installation should be as declarative as everything Flux manages
- **cluster-specific placement is needed** — node pools, tolerations, affinity on the Flux
  controllers themselves — and maintaining those as patches over bootstrap output is tiresome
- upgrades happen often enough that "re-run the CLI at the right version" is a real risk
- more than one cluster, where drift between installations is otherwise invisible
- you want one object to answer "is Flux healthy" (`FluxReport`)

## When not to use it

- a single cluster, installed once, rarely upgraded — `flux bootstrap` is upstream, documented and
  enough
- adding a third-party operator to manage a first-party operator is not a trade you want to make
- you are already on a Flux distribution that installs itself another way
- strict policy about the provenance of cluster-privileged controllers; this one is outside the Flux
  organisation

## Notes

### Creating the GitHub App

<https://fluxcd.io/flux/installation/bootstrap/github/#github-organization>

The `FluxInstance` syncs over HTTPS with `provider: github`, which means GitHub App authentication
rather than a deploy key. The App is created once and installed on the organisation or account; two
identifiers come out of that, and the recorded way of keeping them to hand:

```sh
echo 'export PIKAKUBE_FLUX_OPERATOR_APP_ID=xxxxxxx' >> ~/.bashrc
echo 'export PIKAKUBE_FLUX_OPERATOR_INSTALLATION_ID=xxxxxxx' >> ~/.bashrc
source ~/.bashrc
```

These are **identifiers, not secrets** — safe in a shell profile. The third piece, the App's private
key, is not: it lives in `pikakube-flux-operator.private-key.pem` in this folder, and that file is
listed in the repository's `.gitignore`. That arrangement is correct and worth stating explicitly,
because a `.pem` sitting in a GitOps directory is exactly the kind of thing that gets committed by
accident. Verify it stays ignored before adding anything else to this folder.

The three values become the `flux-system` Secret referenced by `spec.sync.pullSecret`.

Why an App rather than a deploy key: App permissions are scoped and revocable at the organisation
level and the token it mints is short-lived. A deploy key is a static credential that nothing
rotates. This is the same argument recorded in [`argocd/`](../../argocd/README.md).

### Checking the installation

```sh
kubectl get fluxreport/flux -n flux-system -o yaml
```

The `FluxReport` is the operator's own status object. It reports the distribution version actually
running, each controller's image and readiness, the sync source and its last successful revision,
and any reconciler errors — all in one place. This is the first command to run when Flux appears to
be doing nothing, because it separates "Flux is broken" from "Flux is fine and your manifest is
wrong".

### Monitoring

<https://github.com/fluxcd/flux2-monitoring-example/tree/main/monitoring/configs/dashboards>

The upstream Grafana dashboards for Flux, recorded as a commented-out reference. They pair with the
`serviceMonitor.create: true` value that is present but **commented out** in the checked-in
`HelmRelease`. So the intent was recorded and not enabled: the dashboards exist upstream, the
ServiceMonitor that would feed them is one uncommented line, and neither is active.

That is a small, cheap gap. Flux exposes reconciliation duration, failure counts and suspension
state as metrics, and without them a `HelmRelease` that has been failing for a week looks exactly
like one that is fine.

### Agent skills

<https://github.com/fluxcd/agent-skills>

An upstream repository of skills for AI coding agents working with Flux — packaged instructions for
reasoning about Flux CRDs, debugging reconciliation and writing manifests. Recorded as a bookmark
rather than as something in use here.

### What is checked in

The `HelmRelease` pulls chart `flux-operator` from an `OCIRepository` at
`oci://ghcr.io/controlplaneio-fluxcd/charts/flux-operator`, tag `0.24.1` — an OCI artefact rather
than a Helm index, which is the direction Flux packaging has moved.

The `FluxInstance` records four decisions worth reading:

| Field | Value | Why it matters |
|---|---|---|
| `distribution.version` | `2.x` | tracks the 2 series; upgrades arrive without a commit |
| `components` | source, kustomize, helm, image-reflector, image-automation | **notification-controller is commented out** |
| `sync` | GitHub App → `andreyolv/pikakube`, `refs/heads/main`, path `clusters/dev`, every 1m | the cluster's entry point |
| `kustomize.patches` | every Deployment onto the `system` node pool, with tolerations and `safe-to-evict: true` | keeps Flux off application nodes |

Two of those deserve a second look:

- **`version: "2.x"`** floats. It gives free patch upgrades and it also means the running version can
  change without anything changing in Git — a soft conflict with the GitOps principle that the
  repository describes the cluster. Reasonable for a lab, worth pinning for anything else,
  particularly given the v2.7 upgrade procedure noted in [`flux/`](../README.md).
- **`safe-to-evict: "true"`** on the Flux Deployments tells the cluster autoscaler it may drain the
  node they are on. That is the right call for controllers that reconcile from Git and hold no
  state, and it is the kind of detail that only gets added after an autoscaler has refused to scale
  down a node for a week.

---

[← Flux](../README.md)
