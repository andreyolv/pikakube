[← Kustomize examples](../README.md)

# namePrefix

Prefixes the name of every resource.

```yaml
resources:
  - ../../base
namePrefix: dev-
```

`ubuntu` becomes `dev-ubuntu`, `my-secret` becomes `dev-my-secret` — visible in
[`output.yaml`](output.yaml).

The part that matters is what it does *not* stop at: Kustomize also rewrites **references** to
the renamed resources. A `volumes[].secret.secretName` or an `envFrom.configMapRef` pointing at
`my-secret` is updated to `dev-my-secret`, because Kustomize parses the documents and knows which
fields are name references. A string-templating tool cannot do this.

Labels are untouched, so selectors keep working.

The common use is deploying several copies of the same base into **one namespace** without
collisions.

Produced with:

```bash
kustomize build overlays/dev -o output.yaml
```

---

[← Kustomize examples](../README.md)
