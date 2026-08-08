[← CNI](../README.md)

# Cilium

<https://github.com/cilium/cilium>
<https://github.com/cilium/hubble>
<https://github.com/cilium/hubble-ui>
<https://artifacthub.io/packages/helm/cilium/cilium/>
<https://github.com/cilium/cilium/blob/master/install/kubernetes/cilium/values.yaml>

Context and comparison against the other CNIs: [../README.md](../README.md)

---

## The problem it solves

Pod networking with an **eBPF dataplane** instead of iptables. Beyond satisfying the
Kubernetes network model, that unlocks things the classic plugins cannot do:

- **kube-proxy replacement** — Service resolution stops degrading as Service count grows
- **L7-aware NetworkPolicy** — policy on HTTP methods and paths, not just IP and port
- **Hubble** — flow-level observability, with a UI, without deploying a separate tracing stack
- **Cluster Mesh** — cross-cluster connectivity without a separate tool, if Cilium runs everywhere
- transparent encryption, and overlay *or* native routing

## When to use it

- you want the most capable dataplane available and will accept the learning curve
- Service count is high enough that iptables becomes the bottleneck
- network observability matters and you would otherwise bolt on another tool
- you plan to replace kube-proxy

## When not to use it

- the team has no appetite for eBPF, or the kernel version cannot be controlled
- a local throwaway cluster where [kindnet](../kindnet/) is already enough
- you specifically need BGP into an existing fabric with a long operational track record — [Calico](../calico/) is the safer pick there

---

## Notes

Install on Kind: <https://docs.cilium.io/en/stable/installation/kind/>

```bash
kind load docker-image quay.io/cilium/cilium:v1.16.5 --name pikakube
```

### WSL caveat

Cilium has problems on WSL — the WSL kernel version has to be updated first.

```bash
# check the current kernel
uname -r
# 5.15.153.1-microsoft-standard-WSL2
```

References for the WSL issue and for Kind setups:

- <https://github.com/cilium/cilium/issues/17745#issuecomment-1004299480>
- <https://dev.to/cslemes/usando-cilium-no-wsl-a1>
- <https://medium.com/@charled.breteche/kind-cluster-with-cilium-and-no-kube-proxy-c6f4d84b5a9d>
- <https://medium.com/@nahelou.j/play-with-cilium-native-routing-in-kind-cluster-5a9e586a81ca>

---

[← CNI](../README.md)
