[← Kustomize examples](../README.md)

# labels

The explicit replacement for [`commonLabels`](../commonLabels/README.md): the same labelling, with
the reach stated rather than implied.

```yaml
resources:
  - ../../base
labels:
  - pairs:
      someName: someValue
      owner: alice
      app: bingo
    includeSelectors: true
    includeTemplates: true
```

| Field | Effect |
|---|---|
| `pairs` | the labels to apply |
| `includeSelectors` | write them into `spec.selector` too — **immutable once created** |
| `includeTemplates` | write them into `spec.template.metadata.labels` (pod labels) |

Both flags default to **false**, which is the whole reason to use this form. `commonLabels`
always writes selectors; here you say so.

The useful pattern is two entries: one with `includeSelectors: true` for the small set of
identifying labels that define the workload, and one with both flags false for everything
descriptive — team, cost centre, owner — which you will want to change later without deleting the
`Deployment`.

Note that `app: bingo` here overwrites the base's own `app: ubuntu`, including in the selector.
Overriding an existing selector label is exactly the operation that fails on a live cluster.

Rendered result in [`output.yaml`](output.yaml):

```bash
kustomize build overlays/dev -o output.yaml
```

---

[← Kustomize examples](../README.md)
