[← Add-ons](../README.md)

# Sveltos addon-controller

<https://github.com/projectsveltos/addon-controller>
<https://github.com/projectsveltos/helm-charts>

---

## The problem it solves

Project Sveltos deploys add-ons to **sets of clusters selected by label**. A `ClusterProfile`
declares which Helm charts, raw manifests, Kustomize outputs or resources should exist, and which
clusters they belong on — `env=production`, `region=eu`, `gpu=true`. Register a new cluster with
matching labels and it receives everything that applies, in the declared order, with drift corrected
continuously.

It is built for the [Cluster API](../../provision/cluster-api/README.md) world, where clusters are
custom resources and creating one is applying YAML. In that world, editing a GitOps directory
structure by hand for every new cluster stops making sense.

## When to use it

- Many clusters, created and destroyed as a routine operation
- Add-on sets that vary by cluster label — hardware, region, environment, tenant
- Alongside Cluster API, where it is the natural companion
- Event-driven deployment: add-ons triggered by something happening in a managed cluster

## When not to use it

- A handful of long-lived clusters — Flux or Argo CD with one path per cluster is simpler
- Where a second reconciliation system alongside the existing one is unwelcome
- Without a clear owner per add-on; two systems installing the same chart will fight
- If the ordering between add-ons has not been thought through

## Notes

Recorded as two links and no commentary:

- <https://github.com/projectsveltos/addon-controller> — the controller
- <https://github.com/projectsveltos/helm-charts> — the charts to install it

The chart living in a separate repository is a recurring pattern in this inventory — see also
[Kubevious](../../../managed/dashboards/kubevious/README.md) and
[Koordinator](../../../managed/scheduler/koordinator/README.md) — and it has the same practical
consequence each time: the chart's versioning and issues are tracked apart from the project's.

**What the model actually gives you** over a GitOps directory per cluster:

- **Selection by label rather than by path.** A new cluster labelled `env=staging` receives the
  staging add-on set with no repository change. That is the whole argument.
- **Ordering and dependencies** between add-ons, declared in the profile.
- **Multi-tenancy** over which profiles may target which clusters, which matters once several teams
  are deploying to a shared fleet.
- **Drift detection** on the managed clusters, not just on the management cluster.

**The thing to be careful about**, and it applies to every tool of this kind: it is a **second
reconciler**. If Flux also manages anything on those clusters, the boundary between them has to be
explicit — per namespace, per resource kind, or per add-on. Two controllers reconciling the same
object is not a race that resolves; it is a loop that continues indefinitely, and the symptom is a
resource that changes every few minutes for no visible reason.

Sveltos is a CNCF Sandbox project. As with everything in this folder, it addresses a problem this
repository does not yet have — and it is recorded because the day Cluster API is adopted is the day
the problem appears.

---

[← Add-ons](../README.md)
