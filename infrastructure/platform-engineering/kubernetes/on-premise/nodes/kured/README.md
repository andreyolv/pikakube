[← Nodes](../README.md)

# kured

<https://github.com/kubereboot/kured>
<https://github.com/kubereboot/charts>

---

## The problem it solves

Kubernetes Reboot Daemon. Kernel and OS security patches require a reboot, and a cluster has no
opinion about when. Left alone, either the patches accumulate unapplied, or someone reboots several
nodes at once and takes out more capacity than the workloads can survive.

kured runs as a DaemonSet, watches for the OS's **reboot-required sentinel file**
(`/var/run/reboot-required` on Debian and Ubuntu), and when it finds one: acquires a **cluster-wide
lock** so only a bounded number of nodes proceed, cordons and drains the node, reboots it, and
uncordons it when it comes back.

## When to use it

- Self-managed nodes with an OS whose package manager signals that a reboot is needed
- Fleets where reboots must be coordinated rather than simultaneous
- A defined maintenance window, and optionally a Slack notification when reboots happen
- Anywhere unattended-upgrades or equivalent is applying kernel patches

## When not to use it

- Managed clusters, where node upgrades are the provider's mechanism
- **Without PodDisruptionBudgets** — see below
- Immutable operating systems such as Talos, where updates are image swaps and this model does not apply
- Where a drain would be disruptive and nobody has decided what the acceptable window is

## Notes

**Chart from a separate repository** — <https://github.com/kubereboot/charts>, distinct from the
project — which is why both links are recorded. Deployed here with a `HelmRelease`, a
`HelmRepository` and a namespace manifest, values empty.

**The lock is the whole design.** kured coordinates through an annotation on a shared object,
functioning as a distributed lock: a node must hold it to reboot, and it is released when the node
returns healthy. Without that, every node that patched at the same time — which is all of them, since
package updates are usually scheduled identically — would reboot simultaneously.

The lock's concurrency is configurable. Raising it above one makes reboots faster and is precisely
the knob that turns coordinated maintenance back into an outage.

**PodDisruptionBudgets are not optional here.** kured drains before rebooting, and `drain` respects
PDBs. Without them, a drain evicts every pod on the node immediately, and with a three-replica
service spread over three nodes being rebooted in sequence, the service may have no healthy endpoints
during each transition. With PDBs, the drain waits — which is what you want, and which is also why a
badly written PDB (`minAvailable: 100%`) blocks reboots entirely.

**Things worth configuring before it runs unattended:**

- **A maintenance window** — `--reboot-days`, `--start-time`, `--end-time`, and a timezone. Reboots at
  03:00 on a Tuesday are a different proposition from reboots at 14:00 on a Friday.
- **A notification** — the Slack or webhook integration, so reboots are observed rather than
  discovered.
- **`--reboot-sentinel`** if the OS signals differently; the default is Debian/Ubuntu's convention.
- **Blocking conditions** — kured can refuse to reboot while a given Prometheus alert is firing or
  while pods matching a selector are running. That is the mechanism for "not during a batch job".

**The alternative worth knowing about** is not to reboot at all: an immutable OS such as Talos
replaces the running image rather than patching it, which removes this entire category of tooling.
See [`local/linux/distribution/`](../../../local/linux/distribution/README.md).

---

[← Nodes](../README.md)
