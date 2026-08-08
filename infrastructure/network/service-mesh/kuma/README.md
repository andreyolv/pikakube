[← Service mesh](../README.md)

# Kuma

<https://github.com/kumahq/kuma>
<https://kuma.io/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

An Envoy-based mesh whose distinguishing trait is that it was designed for **Kubernetes and
VMs together**, rather than Kubernetes with VM support added afterwards.

Its control plane treats both as first-class data plane proxies, and it supports multi-zone
topologies across clusters and datacentres from the same model.

## When to use it

- the estate is **not entirely Kubernetes** — services still run on VMs and need to be in the same mesh
- multi-zone across clusters or datacentres, without stitching together per-cluster meshes
- you want Envoy's capabilities with a simpler control plane than Istio's

## When not to use it

- everything already runs in Kubernetes — [Linkerd](../linkerd/) or [Istio](../istio/) have larger communities and more material for that case
- Consul is already deployed, which covers the mixed-estate case with what you have

---

## Notes

```bash
kubectl port-forward svc/demo-app -n kuma-demo 5000:5000
kubectl port-forward svc/kuma-control-plane -n kuma 5681:5681
```

GUI: <http://127.0.0.1:5681/gui/>

---

[← Service mesh](../README.md)
