[← Dashboards](../README.md)

# KubeView

<https://github.com/benc-uk/kubeview>

---

## The problem it solves

Most dashboards give you lists. KubeView gives you a **picture**: a live force-directed graph of a
namespace showing Deployments, ReplicaSets, Pods, Services, Ingresses and their relationships, with
node colour indicating health.

Its real audience is people learning what the objects are and how they connect. Seeing that a Service
selects Pods which belong to a ReplicaSet owned by a Deployment — as a diagram that redraws when
something changes — teaches the ownership model faster than any amount of `kubectl describe`.

## When to use it

- Explaining Kubernetes object relationships to someone new
- A quick visual check that a Service actually selects the Pods you think it does
- Demos and teaching, where a live diagram lands better than terminal output

## When not to use it

- Day-to-day operations; the graph does not scale past a small namespace
- Editing anything — it is read-only by design
- Large clusters, where the picture becomes an unreadable hairball
- As the primary dashboard for a team

## Notes

**Installed from a `GitRepository`, not a Helm repository.** The Flux source points at
`https://github.com/benc-uk/kubeview.git` pinned to tag `0.1.31`, and the `HelmRelease` references
the chart by path: `chart: charts/kubeview`.

That is the mechanism to note. The project does not publish a packaged chart to a Helm repository, so
Flux clones the Git tag and builds the chart from the tree. Flux supports this directly and it is
the correct pattern for charts that live only in a source repository — but it changes the upgrade
story: there is no chart index to watch, so version bumps mean editing the Git tag.

Upstream references kept as comments in the release:

- `https://artifacthub.io/packages/helm/kubeview/kubeview`
- `https://github.com/benc-uk/kubeview/blob/master/charts/kubeview/values.yaml`

No notes were recorded beyond the project link.

**Check the project's activity before relying on it.** KubeView is a single-maintainer project and
the pinned `0.1.31` tag is doing real work here — a version pin against a repository that may not
move again. For a teaching tool that is entirely acceptable; the reason to write it down is so nobody
plans a platform around it.

If the relationship graph is what appeals but the questions are operational rather than educational,
[Kubevious](../kubevious/README.md) covers similar ground with configuration validation attached.

---

[← Dashboards](../README.md)
