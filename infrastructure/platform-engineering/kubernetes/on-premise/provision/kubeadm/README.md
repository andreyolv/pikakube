[← Provision](../README.md)

# kubeadm

<https://github.com/kubernetes/kubeadm>

---

## The problem it solves

kubeadm is the upstream tool that bootstraps a conformant Kubernetes control plane. `kubeadm init`
generates the certificates, writes the static pod manifests for the API server, controller manager,
scheduler and etcd into `/etc/kubernetes/manifests`, and starts them via the kubelet.
`kubeadm join` adds nodes. `kubeadm upgrade` moves the cluster between versions.

Deliberately, it does **not** install a CNI, a CSI driver, an ingress controller or anything else. It
produces a working control plane and stops, leaving every other decision to you.

## When to use it

- Learning what a Kubernetes cluster is actually made of
- Small self-managed clusters where automation is not yet justified
- Debugging what [Kubespray](../kubespray/README.md) or
  [Cluster API](../cluster-api/README.md) are doing, since both use it underneath
- The certification path — CKA assumes it throughout

## When not to use it

- Many clusters, or clusters created frequently — that is automation's job
- Where no one will own certificate rotation, upgrades and etcd
- As a production process performed by hand, repeatedly, from memory
- Managed clusters, where none of this is yours

## Notes

Recorded as a link only. The substance lives in the
[CKA notes](../../../managed/core/certifications/cka/README.md), which contain the installation
references and the full upgrade sequence — control plane drained, `kubeadm upgrade plan`,
`kubeadm upgrade apply`, kubelet and kubectl packages, `daemon-reload`, `systemctl restart kubelet`,
`uncordon`; then workers with `kubeadm upgrade node`.

**Why it is worth doing by hand once**, even if the destination is automation: kubeadm makes the
architecture visible in a way nothing else does.

- **The control plane runs as static pods.** `/etc/kubernetes/manifests` holds the API server,
  controller manager, scheduler and etcd manifests; the kubelet watches that directory and starts
  whatever is in it, with no API server involved. That is why the control plane can start before
  there is a control plane, and it is also a recovery route when the API server is down.
- **Certificates live in `/etc/kubernetes/pki`.** `ca.crt` and `ca.key` are the root of all cluster
  identity — the same files the CKA notes use to sign a user certificate. Anyone with `ca.key` can
  mint an administrator.
- **They expire, typically after one year.** `kubeadm certs check-expiration` reports it, and
  `kubeadm certs renew` handles it. A cluster that has run for a year without an upgrade — which
  silently renews them — stops working on an anniversary nobody recorded.
- **kubeconfigs are generated**, not configured: `admin.conf`, and per-component configs, all built
  from that CA.

**The thing kubeadm does not do** is the most important sentence about it: after `kubeadm init`
completes, every node is `NotReady` and every pod is `Pending`, because there is no CNI. That is not
a failure. Installing a network plugin is the first of the decisions kubeadm deliberately leaves to
you, and the confusion it causes on a first attempt is a useful lesson about how little Kubernetes
assumes.

---

[← Provision](../README.md)
