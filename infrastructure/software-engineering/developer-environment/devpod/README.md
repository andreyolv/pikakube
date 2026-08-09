[← Developer environment](../README.md)

# DevPod

<https://github.com/loft-sh/devpod>

---

## The problem it solves

DevPod takes a `devcontainer.json` and provisions the environment it describes **anywhere** — a
local Docker daemon, a Kubernetes cluster, a cloud VM, or an SSH host — then connects a local
editor to it. Its own description is "Codespaces, but open source, client-only and unopinionated".

The two words doing the work there:

**Client-only.** There is no server to install, no control plane, no database. DevPod is a binary
on the developer's machine that talks directly to the provider's API. Compare that with
[Coder](../code-server/README.md), where the platform itself is a service the team then has to
operate and keep available. DevPod has nothing to go down.

**Unopinionated.** The provider is pluggable. The same `devcontainer.json` runs on Docker today and
on Kubernetes next month, and the definition does not change — which is the property that keeps the
choice reversible.

The editor stays local. Unlike code-server, VS Code (or an IDE over SSH) runs on the laptop and
attaches to the remote environment, so the local keybindings, settings and extensions come along.

## When to use it

| Situation | Why |
|---|---|
| **Remote environments without running a platform** | client-only; nothing to operate |
| **A local editor is non-negotiable** | the editor stays local and attaches remotely |
| Work that needs more machine than a laptop | provision a large instance for the duration |
| Environments on several backends | one definition, many providers |
| Evaluating remote development at all | the cheapest way to find out whether the team wants it |
| A devcontainer definition already exists | it is the input format — nothing new to write |

## When not to use it

| Situation | Use instead |
|---|---|
| Local Docker is enough | a [devcontainer](../devcontainer/README.md) directly — DevPod adds nothing |
| **Browser-only access is required** | [code-server / Coder](../code-server/README.md) — DevPod assumes a local editor |
| Central control of who gets what, with quotas and auditing | a managed platform; client-only means policy lives on each client |
| Cost control across a team | each developer provisions independently; there is no central ceiling |

That last pair is the honest trade. Client-only removes the operational burden by removing the
central point of control — which is exactly what you want for a handful of developers and exactly
what you lose when you need governance.

## Notes

The original note is the repository link alone. What it is worth recording alongside it:

**It consumes the same `devcontainer.json` as VS Code and Codespaces.** That is the reason this
tool belongs in a folder next to [`devcontainer/`](../devcontainer/README.md) rather than competing
with it. The definition is the portable asset; DevPod is one of several things that can read it. A
project with a working devcontainer can be tried on DevPod with no changes to the repository.

**The Kubernetes provider is the one that matters here.** It runs the workspace as a pod in a
cluster, which means the environment resolves in-cluster services by their internal DNS names with
no VPN and no port-forwarding — the same network-position advantage as Coder, without deploying a
control plane to get it.

**Workspaces stop and start.** The provisioned machine can be shut down when idle and brought back
with its state, which is what keeps a cloud provider's bill from growing quietly. It is opt-in
behaviour worth configuring on day one rather than after the first invoice.

Nothing here is deployed; this is a reference. The prerequisite for trying it is a working
devcontainer definition, which is the same prerequisite everything else in this folder has.

---

[← Developer environment](../README.md)
