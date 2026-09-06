[← Platforms](../README.md)

# Cyclops

<https://github.com/cyclops-ui/cyclops>

---

## What it actually is

A **form generator over Helm charts**. The platform team points Cyclops at a chart; Cyclops reads
its `values.schema.json` and renders a web form with the right fields, types and validation. A
developer fills in the form, and a controller turns the result into a `Module` custom resource,
renders the chart, and applies the objects.

That places it in the [package management UI](../README.md#1-four-different-products-in-one-folder)
category alongside [Kubeapps](../kubeapps/README.md) and
[Helm Dashboard](../helm-dashboard/README.md) — but with a different emphasis, and the difference
is the point:

| | Kubeapps | Helm Dashboard | Cyclops |
|---|---|---|---|
| Question it answers | "what can I install from the catalog?" | "what is deployed, and why is it broken?" | "how do I configure **our** application?" |
| Values are | a YAML editor over the chart's defaults | inspected and diffed | **a generated form, bounded by a schema** |
| Audience | anyone browsing a catalog | an operator debugging a release | a developer who does not want to see YAML |

The schema is what makes it interesting. A `values.yaml` text box hands the developer the entire
surface of the chart and hopes they edit the right three lines. A schema-generated form exposes
only what the platform team decided to expose, with validation attached — the abstraction is
defined by the chart author rather than by the UI.

## The consequence worth understanding

Configuration state lives in the cluster, in the `Module` resource, because that is what the
controller reconciles. A developer changing a field through the UI changes a cluster object.

For a repository built on GitOps this is the question that decides everything. The
[GitOps folder](../../../../gitops/README.md) exists on the premise that Git is the source of
truth and the cluster is derived from it. A UI that writes configuration directly into the cluster
inverts that, and the two models do not merge on their own — you get drift, or you get Flux
reverting what the developer just did.

There are ways to reconcile them (drive the `Module` resources themselves from Git, and use the
UI as a read-and-propose surface), but that is a design decision to make deliberately before
adopting it, not a detail to discover afterwards.

## When to use it

- the platform team maintains a small set of **internal charts**, and developers should configure
  them without learning Helm
- `values.schema.json` already exists, or writing one is acceptable — without a schema the form
  degrades to a generic editor and most of the value goes with it
- the alternative today is copy-pasting last service's `values.yaml` and changing the name

## When not to use it

- **GitOps is the delivery model and no one has decided how the two coexist.** See above; this is
  the disqualifying question, not a caveat
- the requirement is a catalog of third-party applications to self-install —
  [Kubeapps](../kubeapps/README.md) is built for that
- the requirement is debugging existing releases — [Helm Dashboard](../helm-dashboard/README.md)
- developers already work comfortably in Helm values, in which case this adds a component and
  removes nothing

## Notes

Nothing deployed — recorded from <https://github.com/cyclops-ui/cyclops>, Apache 2.0. It installs
as a controller plus a UI, so it is genuinely small compared to most of this folder: closer to
"an afternoon" than to the distributions in §1.

**Where this lands for pikakube.** The [folder's verdict](../README.md#6-how-this-applies-to-pikakube)
is that the platform here is being assembled deliberately rather than adopted as a product, and
that verdict is unchanged — but Cyclops is the narrowest and cheapest thing in the folder, and the
only one that does not ask to own ingress, GitOps or monitoring.

The blocker is not size, it is direction: this repository delivers through Flux, and Cyclops writes
to the cluster. Until there are developers who need a form — and the
[IDP folder](../../../../idp/README.md) is clear that there are no users yet — the question does not
arise. If it does, the schema-driven form is the idea worth keeping even if the tool is not: a
bounded set of fields beats a `values.yaml` text box regardless of what renders it.

---

[← Platforms](../README.md)
