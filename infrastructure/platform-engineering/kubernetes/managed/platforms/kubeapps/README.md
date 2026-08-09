[← Platforms](../README.md)

# Kubeapps

<https://github.com/vmware-tanzu/kubeapps>

---

## The problem it solves

A web catalog for installing applications into a cluster. Kubeapps presents Helm repositories — and
other package formats through its plugin system — as a browsable catalog with a form-driven values
editor, then tracks what is installed and offers upgrades and rollbacks.

The point is **self-service**: a developer installs a database or a monitoring stack from a UI
instead of filing a ticket, with the catalog constrained to what the platform team has approved.

## When to use it

- Self-service installation from a **curated** catalog you control
- Teams that should install approved software without learning Helm
- A visual view of what is installed and which chart version each release is at
- Where the form-driven values editor is genuinely easier than editing YAML

## When not to use it

- A GitOps cluster — UI-driven installs are drift by definition
- With an uncurated public catalog; anyone can install anything, with whatever permissions the chart asks for
- If a Helm UI is all you want; [Helm Dashboard](../helm-dashboard/README.md) is far smaller
- Without first checking the project's and its chart source's current status — see below

## Notes

**Chart** `kubeapps` version `2.11.0` from `https://charts.bitnami.com/bitnami`, with a namespace
manifest and empty values. Recorded as a link only.

**The dependency worth flagging is the chart source.** Bitnami's public catalog and image
distribution have been substantially restructured under Broadcom, with parts of the free catalog
moved or restricted. Kubeapps originated at Bitnami, was maintained under `vmware-tanzu`, and its
chart is served from the Bitnami repository — which makes it the entry in this folder most exposed to
that restructuring. Before doing anything with this beyond reading it: verify the chart still
resolves, verify the images it references are still available, and verify the project's current home.

**The RBAC model is its most important property**, and it is a good one: Kubeapps performs actions
**as the logged-in user**, using their token, rather than as a privileged service account. So a user
can only install what their own RBAC permits. That is the correct design, and it means the security
question is not "what can Kubeapps do" but "what can your users do" — which is a question you can
already answer.

**The GitOps conflict is unavoidable.** Kubeapps installs Helm releases directly. Flux installs Helm
releases from Git. A release created through the UI has no representation in the repository; a
release managed by Flux will fight any change made in the UI. There is no configuration that
reconciles these two positions — it is a decision about who owns installation.

Which is why, in this repository, it sits in the inventory rather than in the cluster.

---

[← Platforms](../README.md)
