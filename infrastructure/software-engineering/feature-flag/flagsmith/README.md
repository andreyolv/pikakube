[← Feature flags](../README.md)

# Flagsmith

<https://github.com/Flagsmith/flagsmith>
<https://github.com/Flagsmith/flagsmith-charts>

---

## The problem it solves

Feature flags **and remote configuration** in one system, which is the distinction worth
understanding before choosing between this and [Unleash](../unleash/README.md).

In Flagsmith a flag is not only a boolean — it carries a **value**. So the same mechanism that
turns a feature on also delivers the string, number or JSON blob that configures it, per
environment and per segment:

| What you can change without a deploy | Example |
|---|---|
| A boolean | is the new checkout on |
| A value | how many results per page, which model name, a copy string |
| Per segment | both of the above, different for a plan, a region, a tenant |

**Segments** are the second idea. You define a group by traits — plan is enterprise, country is
BR, app version is above 4.2 — and target flags and values at the group rather than at a
percentage. That is targeting the router in a canary deploy cannot do, because it cannot see who
the user is.

Two repositories, as the note records: `Flagsmith/flagsmith` is the platform and
`Flagsmith/flagsmith-charts` is the Helm chart.

## When to use it

- you want **flags and configuration values together**, rather than a flag system plus a separate
  config mechanism
- **segment-based targeting** by user traits is a real requirement
- a UI for product and support people is the point, not a compromise
- you want a self-hosted option with a managed one available, without changing the API

## When not to use it

- flag state belongs in **Git**, reviewed as a commit — that is [Flipt](../flipt/README.md)
- you do not want a **PostgreSQL** database to run and back up
- remote config values are a temptation you would rather not have: it is easy for what should be
  deployment configuration to drift into a flag system, where it is outside your manifests and
  outside review
- client-side evaluation is the plan without thinking it through — rules and unreleased feature
  names visible in a browser are visible to users

## Notes

**What is deployed here:** chart `flagsmith` 0.61.0 from
`https://flagsmith.github.io/flagsmith-charts/`, in the `flagsmith` namespace, with an empty
`values` block. The Artifact Hub page and the upstream `values.yaml` are linked in comments, which
is the pattern used across this repository — the chart is mapped, not configured.

**It needs PostgreSQL**, like [Unleash](../unleash/README.md). The chart will deploy one; for
anything real that database holds production behaviour and should be run properly — see
[CloudNativePG](../../../databases/sql/postgresql/operator/cnpg/README.md).

**The remote-config capability is the reason to pick it and the reason to be careful.** Values
that change without a deploy are extremely useful for things that legitimately vary by segment,
and a slow leak for things that should have been in a `ConfigMap` and reviewed. Decide the
boundary before adopting it, not after — the anti-pattern table in the
[parent README](../README.md#9-anti-patterns) has this as its own row.

**Put OpenFeature in front of it** — see [`open-feature/`](../open-feature/README.md). The
argument is the same as for every backend in this folder: the vendor decision is the one you want
to keep reversible.

---

[← Feature flags](../README.md)
