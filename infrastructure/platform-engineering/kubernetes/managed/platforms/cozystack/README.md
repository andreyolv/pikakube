[← Platforms](../README.md)

# Cozystack

<https://github.com/cozystack/cozystack>

---

## The problem it solves

Cozystack is aimed at a specific and unusual target: **building a public or private cloud on bare
metal**. It is a platform for hosting providers and for organisations that want to offer
Kubernetes-as-a-service internally, rather than for running applications on a cluster you already
have.

It bundles Talos as the operating system, virtualisation through KubeVirt, storage, networking, and
managed services — databases, message queues — which tenants can provision themselves. Tenants get
their own Kubernetes clusters; you run the substrate underneath.

## When to use it

- You have bare metal and want to offer clusters or managed services to internal teams or customers
- Building a private cloud, where the alternative is assembling KubeVirt, Talos, storage and
  networking yourself
- Hosting providers, which is the primary audience
- Cluster-as-a-service is the product, not the tool

## When not to use it

- You already have a cluster and want to run applications on it — this is the wrong layer entirely
- Managed Kubernetes in a cloud; the whole premise is that you own the hardware
- Without a team that can operate bare metal, storage and networking
- As a comparison against the other distributions here; the audience is different

## Notes

Recorded as a link only, with **no chart and no manifests** — the only entry in this folder installed
by neither Helm nor plain YAML. That reflects how Cozystack is deployed: it is a distribution
installed onto machines, not a chart applied to an existing cluster.

**Its placement in `platforms/` is defensible but the category is different.** Everything else here
sits on top of a cluster. Cozystack *produces* clusters. Its natural neighbours in this repository are
[`on-premise/provision/`](../../../on-premise/provision/README.md) and
[`virtual-machine/kubevirt/`](../../virtual-machine/kubevirt/README.md) — which it bundles — rather
than [KubeSphere](../kubesphere/README.md) or [Devtron](../devtron/README.md).

**The stack it assembles** is the interesting part, because each piece appears independently
elsewhere in this repository: Talos as an immutable node OS
([`local/linux/distribution/`](../../../local/linux/distribution/README.md)), KubeVirt for VMs,
Flux for reconciliation, and per-tenant managed services. Cozystack's contribution is the
integration and the tenant-facing model, not the components.

**Two cautions** for anyone tempted:

- **It is opinionated all the way down to the operating system.** Adopting it means adopting Talos.
  That is a defensible choice and it is not a small one.
- **Operating a cloud is not operating a cluster.** Storage failure domains, network fabric,
  hardware lifecycle and tenant isolation are the actual work, and the platform only helps with the
  last of them.

---

[← Platforms](../README.md)
