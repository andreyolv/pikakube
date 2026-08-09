[← Feature flags](../README.md)

# Flipt

<https://github.com/flipt-io/flipt>
<https://github.com/flipt-io/helm-charts>

---

## The problem it solves

A **lightweight, self-hosted** flag engine whose distinguishing idea is that flag state can be
**declared in files and read from Git** rather than living in a database behind a UI.

That single property changes what a flag system is:

| | **Database-backed** (the usual model) | **Flipt, declared** |
|---|---|---|
| Source of truth | rows in a database | files in a repository |
| How a flag changes | someone clicks in a UI | a commit, reviewed and merged |
| Audit trail | whatever the tool records | `git log` — the one you already have |
| Reproducing an environment | export and import | check out the branch |
| Disaster recovery | restore the database | it is already in Git |
| Speed of a change | seconds | as fast as your pipeline |

For a GitOps repository that is a very good fit, because it removes the exception. Every other
piece of behaviour in this platform is a file that was reviewed and reconciled; with Flipt in
declarative mode, flags stop being the one thing that changes by clicking.

Evaluation is served over **REST and gRPC**, and the server is a single Go binary — small enough
that running it per environment is not a burden.

Two repositories, as the note records: `flipt-io/flipt` is the server and `flipt-io/helm-charts`
is the deployment.

## When to use it

- **a GitOps repository**, where flags should be reviewed and versioned like every other change
- you want a small, self-contained service — no database required in the declarative mode
- gRPC evaluation matters, or the fleet is Go-heavy
- the flags are for engineers, and engineers are the only people who need to flip them

## When not to use it

- **product, support or on-call need to flip a flag in seconds.** This is the real objection: a
  kill switch that requires a merge and a reconcile is not a kill switch. If that capability
  matters, [Unleash](../unleash/README.md) or [Flagsmith](../flagsmith/README.md) is the honest
  choice
- you want remote configuration values alongside flags — that is
  [Flagsmith](../flagsmith/README.md)'s pitch
- you need the largest possible official SDK matrix; the ecosystem is smaller than Unleash's, and
  [OpenFeature](../open-feature/README.md) is how you compensate

## Notes

**What is deployed here:** chart `flipt` 0.77.0 from `https://helm.flipt.io`, in the `flipt`
namespace, with an empty `values` block and the upstream `values.yaml` linked in a comment.
Nothing is configured, so the storage mode — the decision that makes or breaks the fit described
above — has not been made yet. **That is the first choice to make if this is picked up**, because
declarative-from-Git and database-backed are different products in practice.

**The trade-off is worth restating**, because it is the one that decides between the three
backends in this folder and it is not really a feature comparison:

> Git-declared flags are auditable by construction and slow to change.
> UI-driven flags are fast to change and audited only by the tool.

Kill switches want the second. Release toggles are perfectly happy with the first. A platform that
only ever needs release toggles should take the Git model; one that needs an incident response
lever should not.

**Put OpenFeature in front of it** — see [`open-feature/`](../open-feature/README.md). This
matters slightly more for Flipt than for the others, precisely because its SDK ecosystem is
smaller: coding against the standard means the language coverage question is answered by the
provider layer rather than by the vendor.

---

[← Feature flags](../README.md)
