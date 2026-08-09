[← Kustomize examples](../README.md)

# commonLabels

Adds labels to every resource — and to selectors and pod templates as well.

```yaml
resources:
  - ../../base
commonLabels:
  app: my-app
  environment: development
```

In [`output.yaml`](output.yaml) the labels appear in three places on the `Deployment`:
`metadata.labels`, `spec.selector.matchLabels`, and `spec.template.metadata.labels`. That is
required for the thing to work — a `Deployment` whose selector does not match its own pod
template selects nothing.

**The trap:** `spec.selector` is **immutable after creation**. Because `commonLabels` writes into
it, changing or removing a common label later produces a rejected apply, and the only fix is to
delete the `Deployment` and let it be recreated. Treat these labels as permanent from the moment
they are first applied.

That trap is why [`labels`](../labels/README.md) exists — it makes touching selectors an explicit
choice. **Prefer `labels` in new work;** `commonLabels` is the older form and is what most
existing `kustomization.yaml` files still use.

For anything that does not need to be selectable, use
[`commonAnnotations`](../commonAnnotations/README.md) instead: annotations are never part of a
selector, so they can be changed freely.

```bash
kustomize build overlays/dev -o output.yaml
```

---

[← Kustomize examples](../README.md)
