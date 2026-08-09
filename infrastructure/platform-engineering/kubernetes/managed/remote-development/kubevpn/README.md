[← Remote development](../README.md)

# KubeVPN

<https://github.com/kubenetworks/kubevpn>

---

## The problem it solves

A VPN into the cluster network. `kubevpn connect` makes cluster Services, pod IPs and DNS resolvable
from your machine, so a locally running process can talk to in-cluster dependencies as though it were
inside.

It also supports proxy mode — diverting a workload's traffic to your machine, the same idea as a
Telepresence intercept — and can run a local container image with the cluster's environment. But the
tunnel is the core, and it is the simplest framing of this category: no interception semantics, no
operator, just network reachability.

## When to use it

- Local processes need to reach cluster Services and pod IPs
- You want the smallest possible tool for that, without an operator or a licence
- Connecting to several clusters or namespaces at once
- Cluster networking access for tooling rather than for debugging a specific workload

## When not to use it

- Production — a VPN into a production pod network is a serious access decision
- Where interception with per-user routing is the requirement; [Telepresence](../telepresence/README.md) is more developed there
- If a tunnel that changes your machine's routing table is not acceptable on that laptop
- Where `kubectl port-forward`, or `kubefwd` for a whole namespace, would do

## Notes

**Chart** `kubevpn` from the project's Helm repository, with a namespace manifest and empty values.
Recorded as a link only.

**Where it sits between the alternatives** is the useful thing to record, because this folder has
four tools and they are not four versions of the same thing:

| Tool | What it gives you |
|---|---|
| `kubectl port-forward` | one port, one pod |
| [kubefwd](../../README.md) | every Service in a namespace, with `/etc/hosts` entries |
| **KubeVPN** | the whole cluster network, resolvable and routable |
| [Telepresence](../telepresence/README.md) | the network, plus per-user traffic interception |
| [mirrord](../mirrord/README.md) | your process behaves as a pod, with traffic mirrored by default |

The list is roughly in order of invasiveness. KubeVPN is the point at which you stop forwarding
individual things and start joining the network — which is convenient and is also the point at which
your laptop has routes into the cluster's pod CIDR.

**Two practical cautions:**

- **It modifies routing and DNS on your machine**, which usually requires elevated privileges and can
  conflict with a corporate VPN. That conflict is the same class of problem recorded for WSL in
  [`local/linux/wsl/`](../../../local/linux/wsl/README.md), and it resolves the same way: expect to
  fight over routes.
- **Disconnecting matters.** A tunnel left open is standing network access to the cluster from a
  laptop, which is worth treating as the access grant it is.

---

[← Remote development](../README.md)
