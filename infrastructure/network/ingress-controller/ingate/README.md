[← Ingress controller](../README.md)

# InGate

<https://github.com/kubernetes-sigs/ingate>

Context and comparison: [../README.md](../README.md)

---

## What it is

A Kubernetes SIG project aiming at an ingress and Gateway API implementation maintained by
the community itself, rather than by a vendor.

The motivation is straightforward: [ingress-nginx](../ingress-nginx/) is the de facto default
and carries a large maintenance burden, and the community wanted a forward-looking successor
built around the [Gateway API](../../gateway-api/README.md).

## Status

**Early.** No Helm chart yet, which by itself makes it awkward for a GitOps setup where
everything else is a `HelmRelease`.

## When to use it

- to follow where community ingress is heading
- experiments and evaluation

## When not to use it

- anything you depend on today — use [ingress-nginx](../ingress-nginx/) or a mature
  [Gateway API implementation](../../gateway-api/README.md) and revisit this later

Mapped here to be watched, not deployed.

---

[← Ingress controller](../README.md)
