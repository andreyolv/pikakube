[← Kustomize examples](../README.md)

# namespace

Sets the namespace of every resource the overlay pulls in.

```yaml
resources:
  - ../../base
namespace: teste
```

The base declares `namespace: kafka-strimzi` on the `Deployment`; the overlay overrides it. The
`Secret` in the base has no namespace at all and gets one.

The point: **the base does not need to be namespace-agnostic**. Whatever it says is replaced, so
one base can be deployed into as many namespaces as there are overlays — which is the usual way
of running the same thing per environment or per tenant in a single cluster.

Rendered result in [`output.yaml`](output.yaml), produced with:

```bash
kustomize build overlays/dev -o output.yaml
```

---

[← Kustomize examples](../README.md)
