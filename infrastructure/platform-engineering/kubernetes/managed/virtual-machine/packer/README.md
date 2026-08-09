[← Virtual machine](../README.md)

# Packer

<https://github.com/hashicorp/packer>

---

## The problem it solves

Packer builds machine images. Given a base image and a set of provisioning steps — shell scripts,
Ansible, file uploads — it boots a temporary instance, runs them, and captures the result as an AMI,
a qcow2, a VMDK, a Vagrant box, or whatever the target platform wants. The same definition can build
the same image for several platforms at once.

For Kubernetes this matters at one specific point: **what do the nodes boot from?** The alternative to
a pre-built image is configuring nodes after boot, and configuration after boot drifts. A node built
in January and a node built in July run different software, and nobody finds out until one of them
behaves differently.

## When to use it

- Building node images for self-managed clusters — kubelet, container runtime and dependencies baked in
- Golden images shared across environments, versioned and reproducible
- Cutting node boot time by pre-installing rather than post-configuring
- Building the same image for several clouds or hypervisors from one definition

## When not to use it

- Managed clusters, where the provider supplies node images — unless custom node images are supported and needed
- Container images; that is a Dockerfile or a buildpack
- Immutable-by-design operating systems such as Talos, where the OS is the artifact already
- One-off machines, where the build pipeline costs more than it saves

## Notes

Recorded as a link only, with no templates and no commands.

**Why it is in a Kubernetes repository**, stated plainly: it belongs to
[`on-premise/provision/`](../../../on-premise/provision/README.md) in spirit. Bootstrapping a cluster
with `kubeadm`, [Kubespray](../../../on-premise/provision/kubespray/README.md) or
[Cluster API](../../../on-premise/provision/cluster-api/README.md) requires nodes, and nodes require
an image. The Cluster API notes already record
`https://github.com/kubernetes-sigs/image-builder`, which is **Packer with Kubernetes node recipes
on top** — so the tool is implied by the provisioning material whether or not it is named there.

**The pre-baked versus post-configured decision** is the substance:

| | Pre-baked image | Configure after boot |
|---|---|---|
| Boot time | fast — everything is present | slow — downloads and installs |
| Reproducibility | **exact**; the image is the artifact | depends on what the repositories serve that day |
| Air-gapped | works | needs a local mirror |
| Changing a version | rebuild the image | change the configuration |
| Drift | none within an image version | accumulates |

For a cluster of any size, pre-baked wins on every row that matters. The cost is a build pipeline and
an image registry to keep, which is real but bounded.

**Licensing changed.** HashiCorp moved Packer, like Terraform, to the Business Source License. For
building your own images that is unlikely to matter, and it is the reason forks exist and the reason
to check before embedding it in a product. The same shift is what produced OpenTofu in the Terraform
case, and OpenTofu is mapped in this repository under `iac/engine/`.

**Version and record the images.** An image with no version and no record of what went into it is a
node nobody can describe — which is precisely the drift the whole approach exists to eliminate.

---

[← Virtual machine](../README.md)
