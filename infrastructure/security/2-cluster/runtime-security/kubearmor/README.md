[← Runtime security](../README.md)

# KubeArmor

<https://github.com/kubearmor/KubeArmor>

Runtime policy enforcement using Linux Security Modules. The kernel refuses the action instead of
reporting it afterwards.

Policies in this folder: [`kubearmorpolicies/`](kubearmorpolicies/README.md)

---

## The problem it solves

[Falco](../falco/README.md) and [Tracee](../tracee/README.md) observe syscalls through tracepoints:
the syscall executes, the event fires, and the tool reports what already happened. That is detection,
and closing the loop requires something else to act — [falco-talon](../falco/falco-talon/README.md),
or a human.

KubeArmor hooks a different kernel interface. **Linux Security Modules** — AppArmor, SELinux, and
BPF-LSM — are *authorisation* hooks: the kernel asks "may this happen?" before proceeding and takes
no for an answer. That is a categorical difference, not a faster version of the same thing.

The model is an allow/deny policy per workload, expressed as Kubernetes custom resources:

| CRD | Scope |
|---|---|
| `KubeArmorPolicy` | namespaced, selected by pod labels |
| `KubeArmorClusterPolicy` | cluster-wide |
| `KubeArmorHostPolicy` | the node itself, not a container |
| `KubeArmorConfig` | the operator's global defaults |

A policy names what to control and what to do about it:

| Block | Controls |
|---|---|
| `process` | which binaries may execute — `matchPaths`, `matchDirectories`, `matchPatterns` |
| `file` | which paths may be read or written |
| `network` | which protocols may be used |
| `capabilities` | which Linux capabilities may be used |
| `action` | `Allow`, `Audit`, or `Block` |

`kubearmorpolicies/block-pkg-mgmt-tools-exec.yaml` in this folder is the canonical example: pods
labelled `app: nginx` may not execute `/usr/bin/apt` or `/usr/bin/apt-get`. A running web server has
no legitimate reason to install packages, and blocking it removes a standard step from most
post-exploitation playbooks.

`KubeArmorHostPolicy` is the capability nothing else in this folder has: policy on the **node**, not
only on containers. That covers the host processes an attacker reaches after a container escape.

## When to use it

- **You want prevention, not detection.** This is the whole point. If the requirement is "this must
  not happen" rather than "we must know it happened", tracepoint-based tools cannot deliver it.
- **The workload's behaviour is narrow and known.** An allow-list is realistic for a web server, a
  sidecar, or a purpose-built service. That is where LSM policy is at its strongest.
- **You want defence in depth below the container.** Even a compromised, privileged container is
  constrained by what the LSM permits. Admission control cannot help once the pod is running.
- **Node-level policy matters.** Host policies protect the node's own binaries and paths.
- **Compliance requires file integrity protection.** "This directory must not be modified" is a
  direct expression here rather than an alert rule.
- **You want to start safely.** Every policy takes `action: Audit` first, and the default posture is
  configurable globally — as it is in this folder.

## When not to use it

- **You do not know what the workload does.** An allow-list against unknown behaviour is a series of
  production incidents. Run in audit, observe, and build the policy from what you saw — KubeArmor can
  generate a policy from observed behaviour, which is the practical way in.
- **Behaviour is broad or dynamic.** Data workloads are the hard case: Spark spawns JVMs and writes
  to arbitrary scratch paths, Airflow executes whatever a DAG author wrote. Enumerating allowed
  processes and paths for those is not realistic, and a partial allow-list is a false sense of
  security plus a source of outages.
- **The node's kernel does not have a usable LSM.** This is a property of the **host image**, not of
  the cluster. If AppArmor is not enabled and BPF-LSM is not available, enforcement degrades to
  observation. On managed node pools you get whatever the provider's image ships. Check before
  planning around it.
- **A false positive is expensive.** A blocked syscall produces a permission error inside the
  application, and nobody's first hypothesis for "the executor died" is "a security policy denied
  it". The failure is invisible to normal debugging.
- **You want broad detection coverage.** KubeArmor's model is per-workload allow-lists. It is not a
  replacement for Falco's several hundred general detection rules — the two answer different
  questions.
- **Another agent is already deployed.** One kernel-hooking DaemonSet per cluster.

## Notes

Every original note from `doc.md`, translated and explained.

### The demonstration

```bash
kubectl create deployment nginx --image=nginx
POD=$(kubectl get pod -l app=nginx -o name)

kubectl exec -it $POD -- bash -c "apt update && apt install masscan"
```

Three commands that demonstrate the whole tool.

The first creates an nginx Deployment, which carries the label `app: nginx` — the exact selector both
policies in [`kubearmorpolicies/`](kubearmorpolicies/README.md) match on. The second captures the
pod name.

The third is the test, and the choice of package is deliberate: **masscan** is a mass IP port
scanner. Installing a network scanner inside a compromised web server is a textbook
post-exploitation step — establish a foothold, then scan the internal network for what else is
reachable.

With `block-pkg-mgmt-tools-exec.yaml` applied, `apt` never executes: the LSM denies it and the shell
gets a permission error. Without it, the install succeeds and the container now has a scanner.

The command is also a neat illustration of why this layer exists at all. Nothing in the Pod spec is
wrong. Admission control approved it, the image scanner found nothing, the posture tools are happy.
The problem only exists at runtime, in what someone chose to run inside a container that was
otherwise entirely compliant.

Note that `kubectl exec` itself is the other half of the story: it is exactly the action Falco's
"terminal shell in container" rule reports on. The same event, seen by two tools in two different
ways — one reports it, the other refuses what it tries to do.

### How it is deployed here

`helm/helmrelease.yaml` installs `kubearmor-operator` v1.2.0 with no values; the operator then reads
`kubearmorconfig.yaml` to configure the agents.

The configuration in `kubearmorconfig.yaml` is the correct starting posture and worth reading as a
model:

| Setting | Value | Meaning |
|---|---|---|
| `defaultFilePosture` | `audit` | file access outside policy is logged, not blocked |
| `defaultNetworkPosture` | `audit` | same for network |
| `defaultCapabilitiesPosture` | `audit` | same for capabilities |
| `defaultVisibility` | `process,network` | which event types the agents collect |
| `enableStdOutLogs` / `Alerts` / `Msgs` | `false` | events go through the relay, not to container stdout |

**Default posture is the setting that matters most.** With `audit`, anything not explicitly allowed
is logged; with `block`, anything not explicitly allowed is denied. Flipping those three fields to
`block` turns the cluster from allow-by-default to deny-by-default in one edit, and it will break
things immediately unless every workload has a complete policy. Audit is the right default and
changing it should be a deliberate, per-workload decision.

The images are pinned to `stable` with `imagePullPolicy: Always`, which means the agent version can
change under you at any pod restart. For a component that hooks the kernel, a pinned version is
worth more than automatic updates.

There is no `kustomization.yaml` in this folder, and the two policies are applied by hand.

---

[← Runtime security](../README.md)
