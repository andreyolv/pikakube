[← Application authorization](../README.md)

# Permify

<https://github.com/permify/permify>
<https://github.com/Permify/helm-charts>

---

## The problem it solves

Permify is the other Zanzibar-style authorization service in this folder: the same model as
[OpenFGA](../openfga/README.md) — permissions derived from a graph of relationships rather than
stored as grants — with a different schema language and a different project shape.

The model is declared in its own DSL, which some find more approachable than OpenFGA's:

```
entity user {}

entity organization {
  relation admin @user
  relation member @user
}

entity document {
  relation parent @organization
  relation owner  @user

  permission edit = owner or parent.admin
  permission view = edit or parent.member
}
```

The distinction from OpenFGA's DSL is stylistic more than semantic — Permify separates
`relation` (stored edges) from `permission` (computed rules) explicitly, and uses dotted
traversal (`parent.admin`) where OpenFGA uses `from`. Both express the same class of model.

Its API surface covers the same essential queries:

| API | Question |
|---|---|
| `Check` | may this subject perform this action on this object? |
| `LookupEntity` | which objects may this subject act on? — the filtered-list query |
| `LookupSubject` | who may act on this object? |
| `SubjectPermission` | every permission a subject holds on an object |
| `Expand` | the relationship path that produced a decision |

Features it emphasises:

- **Attribute support alongside relationships**, so contextual rules combine with the graph.
- **Schema versioning**, which matters more than it sounds: changing an authorization model in
  production while tuples exist in the old shape is one of the genuinely hard parts of adopting
  ReBAC.
- **Multi-tenancy as a first-class concept**, with tenant isolation built into the API rather
  than modelled inside the schema.
- **A snapshot/consistency token model** for the read-after-write problem described in
  [`../README.md`](../README.md) §4.

## When to use it

- **The same conditions as OpenFGA** — per-object permissions, user-to-user sharing, hierarchy,
  and a "what can this user see?" query on the render path. The test in
  [`../README.md`](../README.md) §3 decides whether *either* is warranted; this section is about
  choosing between them.
- **The schema language suits your team better.** This is a legitimate reason. The model is only
  useful if the people maintaining it can read it, and DSL preference is not trivial for a
  document everyone has to review.
- **Native multi-tenancy is a requirement** and you would rather not model tenants inside the
  schema.
- **Schema versioning matters** because the model will evolve while data exists.

## When not to use it

- **Roles are enough.** Same as everywhere in this folder: `admin` / `editor` / `viewer` over
  resource types belongs in the application.
- **You want the safest ecosystem choice.** [OpenFGA](../openfga/README.md) is CNCF incubating
  with a larger community, more SDKs and stronger modelling tooling. For a component on the
  request path of every authorization decision, governance and community size are usually the
  right tiebreaker.
- **You need broad SDK coverage.** Permify's client libraries are fewer.
- **For Kubernetes API permissions.** [`k8s-rbac/`](../../k8s-rbac/README.md).
- **You cannot budget for a network call per check**, or cannot guarantee tuple writes from every
  code path. Both costs are identical to OpenFGA's and are the real barrier to adoption.

## Notes

**`https://github.com/permify/permify`** — the project, and the only note recorded for this
folder. Go, Apache-2.0, from Permify, a company. Open source with a commercial offering
alongside — a different governance model from OpenFGA's CNCF donation, and worth weighing
deliberately rather than by feature comparison.

What is staged: a `HelmRepository`, a `Namespace` `permify`, and a `HelmRelease` for the
`permify` chart at version `0.5.0`.

The `values` block is **empty** — it contains only a single reference comment pointing at
`https://github.com/Permify/helm-charts/blob/main/charts/permify/values.yaml`, the upstream
values file. Note that unlike the other manifests in this tree there is no ArtifactHub link,
which reflects that the chart is distributed from the project's own repository.

Nothing is configured: no storage engine, no schema, no tenancy setup. As staged this is a
version pin and a namespace.

Two things a working deployment would need beyond the chart:

- **Postgres.** Permify's default in-memory engine loses everything on restart and exists for
  experimentation. Production means a database, with its own backup and availability story — the
  same point made in [OpenFGA](../openfga/README.md)'s notes.
- **A schema, and tuple writes from the application.** The schema is the actual product and it is
  written through the API, not through Helm. And nothing populates the relationship graph
  automatically — every permission-relevant change in the application must write a tuple, or the
  permission data is silently wrong.

For this platform the conclusion is the same as for OpenFGA and is stated fully in
[`../README.md`](../README.md): there is no application here with per-object permissions, so
there is nothing for either service to answer. Between the two, OpenFGA is the one to reach for
if that ever changes.

---

[← Application authorization](../README.md)
