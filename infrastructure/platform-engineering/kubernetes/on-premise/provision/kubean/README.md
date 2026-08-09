[← Provision](../README.md)

# Kubean

<https://github.com/kubean-io/kubean>

---

## The problem it solves

Kubean wraps [Kubespray](../kubespray/README.md) in a Kubernetes operator. Instead of running Ansible
playbooks from a workstation with an inventory file, you apply custom resources describing the
cluster and its hosts, and a controller runs Kubespray in a Job to make it so.

It is the middle position between Kubespray and [Cluster API](../cluster-api/README.md): Kubespray's
breadth of supported CNIs, runtimes and topologies — including air-gapped installation — with a
declarative, GitOps-compatible interface in front of it.

## When to use it

- You want Kubespray's coverage but not Ansible-from-a-laptop as the operational model
- Cluster lifecycle should live in Git and be reconciled
- Several on-premise clusters, where repeating playbook runs by hand does not scale
- Air-gapped or offline installations, which it inherits from Kubespray

## When not to use it

- A single cluster; Kubespray directly is fewer moving parts
- Where Cluster API's providers cover your infrastructure — it is the more established model
- Without a management cluster to run the operator, which is an extra thing to keep alive
- If debugging through two layers — operator, then Ansible — is unappealing

## Notes

**Chart** from the project's Helm repository, with a `HelmRelease`, `HelmRepository` and namespace
manifest, values empty. Recorded as a link only.

**The indirection is the thing to weigh.** A failure surfaces as a custom resource that is not ready,
whose Job failed, whose Ansible run failed at some role. Three layers between the symptom and the
cause. Kubespray alone has two of those layers; Cluster API has a different set entirely.

**Where it sits, precisely:**

| | Kubespray | **Kubean** | Cluster API |
|---|---|---|---|
| Interface | Ansible inventory | **custom resources** | custom resources |
| Creates machines | no | no | **yes**, via providers |
| Component breadth | very wide | very wide | provider-dependent |
| Air-gapped | **supported** | **supported** | varies |
| Maturity | high | moderate | high |

The row that decides it is "creates machines". Cluster API provisions the infrastructure as well as
the cluster; Kubean, like Kubespray, expects the hosts to exist. For bare metal that were racked by a
person, that is not a limitation — the machines exist either way — and Kubean's air-gapped support
may matter more than Cluster API's machine provisioning.

**Origin and maturity:** Kubean comes from DaoCloud and is a smaller project than either of its
neighbours. For something that builds clusters, project health is a first-order consideration —
check it before adopting, and weigh it against the fact that the underlying Kubespray is well
maintained and would remain usable directly if Kubean stalled. That fallback is genuinely reassuring
and is the strongest argument for the wrapper.

---

[← Provision](../README.md)
