[← Karmada](../README.md)

# Karmada operator

<https://github.com/karmada-io/karmada>

---

## The problem it solves

Instead of installing a Karmada control plane with Helm, you install an **operator** that creates and
manages Karmada control planes from a `Karmada` custom resource. Creating a control plane becomes
applying a manifest; upgrading it becomes editing a version field; deleting it becomes deleting the
object.

This is the standard operator argument applied one level up: the thing being managed is itself a
control plane.

## When to use it

- More than one Karmada control plane — per environment, per tenant, per region
- Control planes created and destroyed as a routine operation rather than installed once
- You want lifecycle expressed as a custom resource rather than as Helm state
- Upgrades driven declaratively across several instances

## When not to use it

- A single control plane — the [chart](../karmada/README.md) is fewer moving parts
- When operator-managed lifecycle adds a layer nobody on the team wants to debug
- Before there is a multi-cluster requirement at all

## Notes

**Chart** `karmada-operator` from the project's Helm repository, with a namespace manifest and empty
values. Recorded as a link only.

The mental model to keep straight: **the operator does not federate anything.** It creates Karmada
control planes; those control planes federate clusters. Installing the operator and expecting
multi-cluster behaviour produces a controller sitting idle with no `Karmada` resource to reconcile —
which is the most likely first confusion, and it is a two-layer indirection that the documentation
does not always make obvious.

Two consequences of the operator model worth stating:

- **Failure domains multiply.** A broken operator cannot fix a broken control plane, and a healthy
  operator does not guarantee a healthy one. Two things to monitor rather than one.
- **The upgrade story is the point.** Declaring a target version on a custom resource and letting the
  operator sequence the component upgrades is genuinely better than running `helm upgrade` against
  several control planes and hoping the order was right. That benefit only exists once there is more
  than one.

Both paths are present in this repository so the choice is visible; see the
[parent](../README.md) for the comparison.

---

[← Karmada](../README.md)
