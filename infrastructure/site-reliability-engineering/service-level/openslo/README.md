[← Service level](../README.md)

# OpenSLO

<https://github.com/OpenSLO/OpenSLO>
<https://openslo.com/>

---

> **A specification, not a tool.** Nothing to deploy. It defines how an SLO is written down.

## The problem it solves

Every SLO tool invented its own format. [Sloth](../sloth/README.md) has one, [Pyrra](../pyrra/README.md) has CRDs,
Nobl9 and the commercial platforms have theirs. An SLO written for one does not move to another,
so the definitions — which are the durable part — end up coupled to the tooling, which is not.

OpenSLO is a vendor-neutral YAML specification for SLIs, SLOs, error budgets and alerting
policies. The same role OpenTelemetry plays for telemetry: standardise the definition so the
implementation stays replaceable.

## When it matters

- SLO definitions should **outlive** the tool that evaluates them
- multiple teams or vendors need to agree on one format
- you want SLOs reviewed as specifications rather than as generator input

## When it does not

- one tool, one team, no intention of changing. The abstraction costs more than it returns
- you need something that runs and alerts. This defines; something else evaluates

## How it is actually used

Sloth can consume OpenSLO, and other tools support it to varying degrees. The realistic pattern
is to **write definitions in OpenSLO and generate with Sloth or Pyrra** — keeping the durable
artefact portable while using whichever generator suits today.

Whether that indirection is worth it depends on how likely the tooling is to change. For most
platforms it is not, and saying so is more useful than treating every standard as mandatory.

---

[← Service level](../README.md)
