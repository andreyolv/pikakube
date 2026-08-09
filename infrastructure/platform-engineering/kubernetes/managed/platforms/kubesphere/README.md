[← Platforms](../README.md)

# KubeSphere

<https://github.com/kubesphere/kubesphere>

---

## The problem it solves

A full platform distribution with an unusually complete web console: multi-tenancy with workspaces
and projects, a built-in DevOps pipeline system, service mesh integration, observability, an app
store, and multi-cluster management — all installed onto an existing Kubernetes cluster and driven
from one UI.

Its distinguishing feature is **modularity**. The core installs relatively small, and components
(DevOps, service mesh, logging, events, auditing) are enabled individually. That makes it less
all-or-nothing than most distributions in this folder.

## When to use it

- You want a comprehensive UI-driven platform and are comfortable with its opinions
- Its workspace/project tenancy model matches how the organisation is structured
- A CI/CD system inside the cluster is wanted rather than an external one
- A large existing Chinese-language operational community is an advantage rather than a neutral

## When not to use it

- A cluster already running its own GitOps, ingress and monitoring
- Where the pipeline system would duplicate an existing CI platform
- If UI-driven configuration conflicts with a Git-driven workflow — and here it does
- Small clusters, where the footprint is disproportionate to the benefit

## Notes

**Chart** `kubesphere` version `2.7.0` from `https://charts.kubesphere.io/main`, with a namespace
manifest and empty values. Recorded as a link only.

**The version is worth a second look.** KubeSphere's current major line is 3.x and later; `2.7.0` is
an old release. Whether the chart version corresponds to the platform version depends on the chart —
KubeSphere has historically shipped several charts (`ks-installer`, `ks-core`, `kubesphere`) with
independent versioning. Before this is reconciled anywhere, confirm which chart and which platform
version this actually resolves to. A four-year-old platform distribution installed by accident is an
unpleasant surprise.

**The GitOps tension is real here** and worth being explicit about, because KubeSphere is more
UI-centred than most of its neighbours. Its console is designed for people to create projects, set
quotas, configure pipelines and deploy applications by clicking. In a cluster reconciled by Flux,
every one of those actions is drift — either reverted, or permanently divergent from Git. There is no
comfortable middle position; either the console owns the cluster or Git does.

**The multi-tenancy model** — workspaces containing projects containing namespaces — is genuinely
more expressive than plain namespaces, and it is the reason some teams adopt it. Compare with
[`multi-tenancy/`](../../multi-tenancy/README.md), which reaches the same goal with much smaller,
composable pieces.

---

[← Platforms](../README.md)
