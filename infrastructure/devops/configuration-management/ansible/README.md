[← Configuration management](../README.md)

# Ansible

<https://github.com/ansible/ansible>

---

## The problem it solves

A machine exists and needs packages, users, kernel parameters, systemd units, mounted filesystems
and files in `/etc`. Doing that by hand produces machines nobody can reproduce; doing it with a
shell script produces something that only works on a clean machine and breaks on the second run.

Ansible describes the **desired state of a host** in YAML and converges it. Its two defining
choices are why it won this category:

| Choice | Consequence |
|---|---|
| **Agentless** — SSH plus Python on the target | nothing to install, nothing to keep running, no certificate infrastructure |
| **Push, not pull** — you run it, from wherever | no server required to start; a laptop and an inventory file is a working setup |

Everything else — roles, inventories, Jinja templating, Galaxy collections — is structure on top of
that. Modules are meant to be idempotent, so running the same playbook twice converges rather than
duplicates, though that is a property of each module rather than a guarantee of the tool.

## When to use it

- **bootstrapping the machines that become Kubernetes nodes** — kernel modules, sysctls, container
  runtime, kubeadm or k3s installation, disks, `/etc/hosts`. This is the legitimate and common use
  on a Kubernetes platform
- on-prem hardware and bare metal, where nothing else configures the OS
- network devices, load balancers and appliances, which have collections and no other declarative
  interface
- one-off operational procedures across a fleet: rotate a credential, apply an emergency patch,
  collect a file from every host
- anywhere SSH reaches and an agent would not be tolerated

## When not to use it

- **to configure workloads inside Kubernetes.** Kubernetes already reconciles declared state; a
  push-based tool that mutates it from outside fights the controllers and defeats GitOps. Use
  manifests, [templating](../../templating/README.md), and a GitOps controller
- as a deployment mechanism for containerised applications. `ansible-playbook` invoked from CI to
  `kubectl apply` is a push pipeline wearing a configuration-management costume
- for provisioning cloud infrastructure. Ansible can call cloud APIs, but it has no state file and
  no plan step; that is Terraform/OpenTofu's job — see
  mapped under [platform engineering](../../../platform-engineering/README.md)
- at large scale without care. Push over SSH is `O(hosts)` per run, and runs get slow well before
  they get wrong

## Notes

The only recorded reference is the repository: <https://github.com/ansible/ansible>.

Of the five tools mapped in this folder, Ansible is the one **most likely to still be needed** on a
Kubernetes platform, and for a narrow reason: something has to build the nodes, and the nodes are
not Kubernetes. On managed Kubernetes that job belongs to the provider and Ansible has nothing to
do; on self-managed or on-prem clusters it is unavoidable, and the choice is between Ansible and a
pile of shell scripts.

The honest caveat is that agentless push means there is **no continuous reconciliation**. Drift
between runs is invisible. Ansible tells you the state of a host at the moment you ran it, and
nothing after that — which is precisely the property Kubernetes controllers exist to provide, and
the clearest illustration of why the two models are not interchangeable. The full argument is in
[`../README.md`](../README.md).

---

[← Configuration management](../README.md)
