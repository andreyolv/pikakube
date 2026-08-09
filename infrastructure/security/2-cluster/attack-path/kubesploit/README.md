[← Attack path](../README.md)

# kubesploit

<https://github.com/cyberark/kubesploit>

Context and comparison against the other tools: [../README.md](../README.md)

---

## The problem it solves

The other tools in this folder stop at "here is a path" or "here is a weakness". kubesploit
is the one that answers the question a report reviewer always asks next:

> **Is this actually exploitable, or only theoretically?**

It is a **post-exploitation Command & Control framework** — a cross-platform HTTP/2 C2
server plus agent, written in Go and built on the Merlin C2 project, aimed specifically at
**containerised environments**. The workflow it assumes is the one a real attacker follows:
you already have code running in a container (that is the "post" in post-exploitation), and
now you want to demonstrate what can be done from there.

Its value over a generic C2 is a set of container- and Kubernetes-specific modules, run
through an embedded Go interpreter so modules load and execute dynamically. The published
modules cover the classic escape and pivot techniques:

- **container breakout** — CGroup release-agent escape, kernel-module load, `/var/log`
  escape, and mounting host paths
- a lightweight **kubeletctl** for talking to an exposed kubelet API
- **port scanning** and **service discovery** from inside the cluster network
- **CVE scanning** of the reachable environment

The point is not the exploitation for its own sake. It is that a demonstrated breakout ends
the argument about whether a `privileged: true` pod or an exposed kubelet "really" matters.
It closes the loop from KubeHound's *"this path exists"* to *"and here it is, walked."*

## When to use it

- **Validating** that a defensive control genuinely holds: try the breakout the control is meant to prevent, and confirm it fails. This is the adversarial complement to `pod-security/` and `network-policies/`
- Authorised red-team exercises against a cluster you own or have explicit written scope for
- Turning a KubeHound path into a proof-of-concept, when a finding is being disputed
- Security training and lab work, where seeing an escape actually happen teaches more than reading about it

## When not to use it

- **Without explicit written authorisation.** This is offensive tooling that executes real exploits and establishes C2. Running it against infrastructure you do not own, or outside an agreed scope, is at best a fireable offence and at worst a crime. This is not a linter
- On production, or any shared cluster, outside a formally scoped engagement with a rollback plan
- As a scanner. It is a C2 and exploitation framework, not a reporting tool. For "what is wrong with this cluster" use `posture/`, `manifest-scan/` or `3-container/`
- As a control you leave running. It is a tool you pick up for an exercise and put down again — nothing here belongs in a GitOps reconcile loop
- If you only need to know whether a path *exists*. [KubeHound](../kubehound/README.md) answers that read-only and without touching anything. Reach for kubesploit only when "does the path exist" is settled and "can it be walked" is genuinely in question

## Notes

The original note in this folder was the project link and nothing else:

- <https://github.com/cyberark/kubesploit> — the upstream repository, from CyberArk.

Points worth recording alongside it:

- **Not deprecated, but not fast-moving.** As of writing the latest release is **v0.1.3**,
  and the version numbers make the maturity plain: this is a specialised offensive tool,
  not a broadly maintained platform. Verify the current state before relying on it.
- **Built on Merlin.** It inherits Merlin's HTTP/2 C2 design and adds the Go interpreter and
  the container/Kubernetes module set. If you know Merlin, the server and agent model will
  be familiar.
- **There are no manifests in this folder, deliberately.** kube-hunter ships a `Job`
  because it is a one-shot read-only probe; KubeHound is a read-only collector. kubesploit
  is neither — it is an interactive exploitation session, so there is nothing to reconcile
  and nothing to commit. That absence is the correct state, not a gap to fill.
- **Handle the built agents with care.** Upstream ships compiled, password-protected agents
  in its releases. They are functional malware by design; do not scatter them across shared
  systems.

---

[← Attack path](../README.md)
