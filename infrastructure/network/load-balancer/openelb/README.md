[← Load balancer](../README.md)

# OpenELB

<https://github.com/openelb/openelb>
<https://openelb.io/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

The same problem as [MetalLB](../metallb/): on bare metal, `type: LoadBalancer` has no
controller to assign an external IP. OpenELB is an alternative implementation, supporting
L2, BGP and VIP modes.

It originated in the **KubeSphere** ecosystem, which is the usual reason it gets chosen.

## When to use it

- you already run KubeSphere, where it is the native option
- you want a second implementation to evaluate against MetalLB

## When not to use it

- there is no specific reason to differ from MetalLB — which has a larger community, more
  documentation and more deployments behind it. Being different is not by itself a benefit
  for a component this foundational

## The honest note

Mapped here for comparison. For a new bare-metal cluster with no KubeSphere in the picture,
MetalLB is the safer default, and this folder exists to record that the alternative was
considered rather than missed.

---

[← Load balancer](../README.md)
