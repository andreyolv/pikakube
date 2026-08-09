[← Feature flags](../README.md)

# Unleash

<https://github.com/Unleash/unleash>
<https://github.com/Unleash/helm-charts>

---

## The problem it solves

The most established open-source feature-flag server, and the one with the deepest **activation
strategy** model.

A flag in Unleash is not a boolean. It is a name with a set of strategies attached, and each
strategy decides for whom the flag is on:

| Strategy | Turns the flag on for |
|---|---|
| Standard | everyone |
| Gradual rollout | a percentage, made sticky by a chosen identifier |
| User IDs | a named list |
| Constraints | anything in the evaluation context — plan, region, app version, tenant |

The stickiness property is the one that matters and the one people get wrong when rolling their
own: a percentage rollout has to hash a stable identifier, so the same user keeps the same answer
between requests. Otherwise a "10% rollout" is a feature that flickers on and off for everybody.

Evaluation happens **in-process**. The SDK holds the rule set, refreshes it in the background, and
answers locally — so a flag check is a function call, not a network round trip. That is the model
described in [section 4 of the parent README](../README.md#4-where-the-flag-is-evaluated), and it
is why Unleash does not become a latency dependency of your hot path.

Two repositories, as the note records: `Unleash/unleash` is the server and `Unleash/helm-charts`
is the deployment.

## When to use it

- you want the **most mature** option, with the widest official SDK coverage
- the targeting requirements are real — percentages with stickiness, segments, constraints on
  context — rather than on/off
- non-engineers need to flip flags, in a UI, in seconds
- an environment model matters: the same flag with different states across dev, staging and
  production

## When not to use it

- flag state should live in **Git** and change by pull request — that is
  [Flipt](../flipt/README.md)
- you do not want to run and back up a **PostgreSQL** database for it
- **the edition boundary is a problem.** Some capabilities are reserved for the commercial
  edition, and which ones is a moving target. Confirm that the specific feature you are planning
  around is in the edition you intend to run, before you design against it
- flags plus remote configuration values in one system is the requirement —
  [Flagsmith](../flagsmith/README.md) is closer to that

## Notes

**What is deployed here:** chart `unleash` 5.3.4 from `https://docs.getunleash.io/helm-charts`, in
the `unleash` namespace, with an empty `values` block and the upstream `values.yaml` linked in a
comment for reference. Nothing is configured — no ingress, no database settings, no admin
credentials — so this is a mapped tool rather than a running one.

**It needs PostgreSQL.** The chart can bring its own, and for anything beyond a first look that is
the wrong answer: the flag database holds production state and needs backups, upgrades and
monitoring like any other. This repository maps
[CloudNativePG](../../../databases/sql/postgresql/operator/cnpg/README.md) for exactly that.

**Put OpenFeature in front of it.** Unleash has an OpenFeature provider, so the vendor decision
stays reversible at no real cost — see [`open-feature/`](../open-feature/README.md). Coding
directly against the Unleash SDK at every call site is the thing that makes a later change
expensive.

---

[← Feature flags](../README.md)
