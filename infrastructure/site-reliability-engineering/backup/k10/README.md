[← Backup](../README.md)

# K10 (Veeam Kasten)

<https://www.kasten.io/>

---

> **Commercial.** There is a free tier limited by node count, and beyond that it is licensed.

## What it is

A backup and disaster-recovery **platform** for Kubernetes: policy-driven backup, a UI,
application discovery, multi-cluster management, ransomware protection and compliance
reporting.

It uses [Kanister](../kanister/README.md) underneath for application-consistent operations, which is the
same idea packaged as a product.

## When to use it

- backup is a **compliance obligation** with an audit trail, and a supported product is easier to defend than an assembled stack
- policy management across many namespaces and clusters, with a UI for people who will not write CRDs
- vendor support is worth paying for on the layer you only exercise during a disaster

## When not to use it

- open source is a requirement — [Velero](../velero/README.md) covers most of the same ground
- the cluster is small enough that policies are a few YAML files
- you already run Velero and it works. This is a replacement, not an addition

## The honest comparison against Velero

| | Velero | K10 |
|---|---|---|
| Licence | open source, CNCF | commercial, free tier by node count |
| Application consistency | hooks | Kanister blueprints, built in |
| UI and policy | third-party or none | included, and a real differentiator |
| Multi-cluster | manual | managed |
| Support | community | vendor |

Velero is the technically sufficient answer for most platforms. K10 is bought for the
**operational surface** — policies, reporting and support — rather than for a capability Velero
lacks.

---

[← Backup](../README.md)
