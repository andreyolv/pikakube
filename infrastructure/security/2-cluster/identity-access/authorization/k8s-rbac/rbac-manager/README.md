[← Kubernetes RBAC](../README.md)

# RBAC Manager

<https://github.com/FairwindsOps/rbac-manager>

---

## The problem it solves

**"Nobody can read the YAML."**

RBAC is verbose in a specific, unhelpful way: the *intent* is small and the *objects* are many.
"The data team gets `edit` in three namespaces and `view` in two more" is one sentence, and five
RoleBindings — each a separate object, each repeating the subject, each drifting independently.

Multiply by ten teams and the cluster holds a hundred bindings that collectively express
something nobody can read.

RBAC Manager is an operator with one custom resource, `RBACDefinition`, that declares the intent
once and generates the objects:

```
RBACDefinition:
  subjects: [ the data team's group ]
  clusterRoleBindings: [ view ]
  roleBindings:
    - namespace: analytics    → edit
    - namespace: staging      → edit
    - namespace: production   → view
```

One object in, many out. What that buys, beyond brevity:

| Property | Why it matters |
|---|---|
| **Reconciliation** | it owns the bindings it generates. Delete one by hand and it comes back; remove it from the definition and it is deleted. Plain RBAC has no such loop — a manually created binding lives forever |
| **No orphans** | removing a team from the definition removes every binding for them, everywhere. With plain RBAC, offboarding means finding all of them |
| **Reviewable diffs** | a pull request shows "the data team gained `edit` in production" as one changed line, not five new files |
| **ServiceAccount generation** | it can create the ServiceAccounts too, keeping identity and grant declared together |
| **Namespace label selectors** | "every namespace labelled `team=data`" — bindings appear automatically as namespaces are created |

That last one is the strongest feature in a multi-tenant cluster, because it makes the grant
follow a *rule* rather than a list that someone has to maintain.

## When to use it

- **Many teams across many namespaces.** The value scales with the product of the two; below
  roughly a few dozen bindings it does not pay for itself.
- **Namespaces are created dynamically** — per team, per environment, per tenant — and bindings
  must follow automatically.
- **Access changes need to be reviewable.** A one-line diff in one file is a genuinely better
  review artifact than five new YAML files.
- **Bindings drift.** If people create RoleBindings by hand during incidents, a reconciling
  controller is how that stops being permanent.
- **You already run Fairwinds tooling** — Polaris, Goldilocks, Nova — and want consistency.

## When not to use it

- **A handful of bindings.** Plain RBAC is *clearer* than an abstraction over it. Adding a
  controller and a CRD to manage twelve objects makes the cluster harder to understand, not
  easier.
- **You expect it to make RBAC safer.** It does not analyse anything. A wildcard verb in an
  `RBACDefinition` produces exactly the same over-grant, generated more efficiently. For risk,
  use [kubiscan](../kubiscan/README.md); for minimality, [audit2rbac](../audit2rbac/README.md).
- **Kustomize or Helm already solves the verbosity.** If bindings are templated from a list in
  values, you already have the "declare once" property without a controller.
- **You are not prepared for a controller with RBAC write permissions.** RBAC Manager can create
  and delete Roles and bindings, which makes it a privileged component by necessity. Compromising
  it is compromising cluster authorization. That is an acceptable trade for the value it
  provides, and it should be a deliberate one.
- **Project activity matters.** Check its current maintenance state before depending on it; a
  controller holding RBAC write access is not something to run unmaintained.

## Notes

**`https://github.com/FairwindsOps/rbac-manager`** — the project, and the only note recorded for
this folder. Go, Apache-2.0, from Fairwinds.

What is staged: a `HelmRepository` named `fairwinds-stable` in `flux-system`, a `Namespace`
`rbac-manager`, and a `HelmRelease` for the `rbac-manager` chart at version `1.21.0`, with a
five-minute reconcile interval.

The `values` block contains only the two reference comments — the ArtifactHub page and the
upstream `values.yaml` — and no configuration. That is actually reasonable for this particular
chart: RBAC Manager needs almost no configuration, because all of its behaviour comes from the
`RBACDefinition` resources you create afterwards. Deploying it does nothing on its own.

Two things worth knowing before applying it:

- **It requires broad RBAC write permissions**, which the chart grants it. This is inherent: a
  controller that manages Roles and RoleBindings must be able to write them. Note the connection
  to [`../README.md`](../README.md) §2 — a controller that can create bindings is, in effect, a
  subject that can escalate. It is a legitimate and necessary grant, and it should be understood
  as one rather than approved unread.
- **It only owns what it generates.** Existing hand-created bindings are untouched; it does not
  take over the cluster's RBAC on installation. Migration is incremental, which is the right
  behaviour and worth knowing so it is not mistaken for the tool failing to do anything.

For this platform, the assessment in [`../README.md`](../README.md) stands: there is one cluster,
one operator, and nowhere near enough bindings for the abstraction to pay for itself. A
controller with cluster-wide RBAC write access, deployed to manage a small number of bindings, is
a net increase in both complexity and privileged surface. It is catalogued here for the day the
cluster has teams in it.

---

[← Kubernetes RBAC](../README.md)
