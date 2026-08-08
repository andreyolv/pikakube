[← CNI](../README.md)

# Flannel

<https://github.com/flannel-io/flannel>

Context and comparison against the other CNIs: [../README.md](../README.md)

---

## The problem it solves

The **simplest possible** thing that satisfies the Kubernetes network model: a VXLAN overlay
giving every pod an IP and letting pods reach each other without NAT. Nothing else.

That minimalism is the feature — little to configure, little to debug, little to break.

## When to use it

- you want pod networking and genuinely nothing more
- the team has no capacity to operate a richer CNI
- the cluster has no network segmentation requirement

## When not to use it

> **It does not enforce `NetworkPolicy`.**

This is the decisive limitation and it fails silently. Policy objects apply without error,
report no problem, and enforce nothing. A cluster on Flannel with NetworkPolicies committed
to Git looks segmented and is not.

If segmentation is a requirement — now or plausibly later — that rules Flannel out before
any other consideration. See
[../README.md](../README.md#networkpolicy-support-is-not-universal).

Also not a fit when native routing is wanted: Flannel is overlay only, so you carry the
encapsulation cost and the reduced MTU permanently.

---

[← CNI](../README.md)
