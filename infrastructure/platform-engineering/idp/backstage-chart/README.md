[← Internal developer platform](../README.md)

# Backstage

<https://github.com/backstage/backstage>
<https://github.com/backstage/charts>

---

## The problem it solves

Nobody can answer "what services do we run, who owns them, and where are their docs?" without
asking in chat. Backstage makes that answerable: a **software catalog** built from
`catalog-info.yaml` files that live in each repository, plus **software templates** for
scaffolding new services and **TechDocs** for rendering Markdown alongside the catalog entry.

The catalog is the product. Plugins — CI status, Kubernetes resources, cost — hang off it.

## When to use it

- The organisation is large enough that service ownership is genuinely unclear
- Teams will maintain their own `catalog-info.yaml` — this is not optional
- There is a named owner with time for a TypeScript application, not just a Helm chart
- You want scaffolding templates so new services start consistent

## When not to use it

- Fewer than a handful of teams — a README and a channel beat a portal
- No one owns it; an unmaintained catalog is worse than none, because people trust it once and stop
- You want a links dashboard — [`dashboard-ingress/`](../../kubernetes/managed/dashboard-ingress/README.md) is that, at a fraction of the cost
- You expect it to deploy things; Backstage triggers pipelines, it does not run workloads
- Nobody on the team writes TypeScript — plugin work is application development

## Notes

The chart used here is the community chart from `https://backstage.github.io/charts`, referenced
in the release as `backstage` version `1.9.2`. The values block is present but empty — the
`HelmRelease` carries the upstream references as comments so the configurable surface is one click
away:

- `https://artifacthub.io/packages/helm/backstage/backstage`
- `https://github.com/backstage/charts/blob/main/charts/backstage/values.yaml`

Two things that matter about that chart and are easy to miss:

- **It expects an image you built.** The chart deploys a Backstage app; Backstage does not ship a
  useful generic image, because plugins are compiled in. Adopting Backstage means owning a build
  pipeline for your own app image, not just a `HelmRelease`.
- **It needs PostgreSQL.** The catalog is a database, not a set of files. Anything serious points
  it at a real instance rather than the chart's bundled one.

Folder named `backstage-chart` rather than `backstage` for exactly that reason: what is mapped here
is the **chart**, not a Backstage deployment.

---

[← Internal developer platform](../README.md)
