[← Service mesh](../README.md)

# Consul

<https://github.com/hashicorp/consul>
<https://github.com/hashicorp/consul-k8s>
<https://developer.hashicorp.com/consul>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

Consul is older than the service mesh category. It started as **service discovery and a
key-value store** for mixed infrastructure, and grew a mesh on top of that foundation.

That history is the reason to choose it: it treats VMs, bare metal and Kubernetes as equal
participants, because it supported the first two long before the third existed.

## When to use it

- Consul is **already deployed** for service discovery or configuration — the mesh is then an increment, not a new platform
- the organisation is invested in the HashiCorp stack (Vault, Nomad, Terraform) and wants the integration
- a genuinely mixed estate where Kubernetes is one environment among several

## When not to use it

- starting fresh with **only Kubernetes** — [Linkerd](../linkerd/) or [Istio](../istio/) are more Kubernetes-native and have more community material
- you want the smallest possible mesh; Consul brings discovery and KV whether or not you need them

---

## Notes

```bash
kubectl port-forward svc/consul-ui 8080:80
```

---

[← Service mesh](../README.md)
