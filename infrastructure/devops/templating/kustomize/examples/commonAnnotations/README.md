[← Kustomize examples](../README.md)

# commonAnnotations

Adds annotations to every resource in the overlay.

```yaml
resources:
  - ../../base
commonAnnotations:
  app.example.com/version: v1.0.0
  app.example.com/env: dev
```

The counterpart to [`commonLabels`](../commonLabels/README.md), and the safer of the two:
**annotations are never part of a selector**, so they can be added, changed and removed on a live
resource without the immutability problem that makes changing a common label require deleting the
`Deployment`.

That makes annotations the right place for anything descriptive and volatile — version, commit
SHA, owning team, source repository — and labels the right place only for what genuinely
identifies and selects the workload.

The other reason to prefer them: labels are indexed and constrained (63 characters, restricted
character set), annotations are not. A Git URL or a build number does not fit in a label value.

Note the domain-prefixed keys. Unprefixed annotation keys risk colliding with something the
ecosystem already uses; `app.example.com/...` cannot.

Rendered result in [`output.yaml`](output.yaml):

```bash
kustomize build overlays/dev -o output.yaml
```

---

[← Kustomize examples](../README.md)
