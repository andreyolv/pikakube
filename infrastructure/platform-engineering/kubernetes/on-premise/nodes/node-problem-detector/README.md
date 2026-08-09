[← Nodes](../README.md)

# node-problem-detector

<https://github.com/kubernetes/node-problem-detector>

---

## The problem it solves

The kubelet reports `Ready` when it is running and can reach the API server. It does not report that
the kernel has a deadlock, that the filesystem has gone read-only, that the container runtime is
failing, or that the node has been logging out-of-memory kills for an hour.

node-problem-detector runs as a DaemonSet, watches kernel logs, systemd journal entries and the
runtime's health, matches them against configurable rules, and reports what it finds **into the
Kubernetes API** — as node conditions for permanent problems, and as events for temporary ones.

The value is making an invisible node-level failure into something the API can see, alert on and act
on.

## When to use it

- Self-managed nodes, where nobody else is watching the kernel logs
- Turning "pods on that node keep failing" into a named node condition
- Feeding a remediation controller, or paging a human, with a trustworthy signal
- Detecting the specific failures that leave a node `Ready` and useless

## When not to use it

- Managed clusters, where the provider generally runs an equivalent and repairs nodes itself
- Expecting it to **fix** anything — it detects, and nothing more
- Without deciding what happens when a condition is raised; a permanent condition nobody reads is noise
- As a substitute for node metrics and log collection; it is a complement to
  [`observability/`](../../../../../observability/README.md)

## Notes

**Chart** from the project's Helm repository, with a `HelmRelease` and `HelmRepository`. No namespace
manifest — it is usually deployed into `kube-system`. Recorded as a link only.

**Detection is not remediation, and that gap is the whole operational question.** node-problem-detector
sets a condition such as `KernelDeadlock=True` on the node. Nothing happens next unless something is
watching. The options:

- **Draino** or a similar controller that cordons and drains nodes carrying a given condition
- On cloud providers, a node auto-repair mechanism that replaces the node
- An alert with a named owner, which is the honest minimum

Installing it and not choosing one of these produces a cluster where broken nodes are correctly
labelled as broken and continue serving traffic.

**What it detects out of the box**, roughly: kernel deadlocks, unregistered network devices, tasks
stuck in uninterruptible sleep, out-of-memory kills, filesystem errors including read-only remounts,
container runtime failures, and kubelet problems. The rules are configuration, so anything visible in
the journal or in a log file can be added — including application-specific patterns, though that is
usually the wrong place for them.

**Two kinds of output, and the difference matters:**

- **Node conditions** — permanent problems. They persist and can be used for scheduling decisions and
  taints.
- **Events** — temporary problems. They expire, and they are for humans reading `kubectl describe
  node`.

Getting that classification wrong in a custom rule produces either conditions that never clear or
events nobody sees.

Part of the Kubernetes project proper, which is a good signal for something running privileged on
every node.

---

[← Nodes](../README.md)
