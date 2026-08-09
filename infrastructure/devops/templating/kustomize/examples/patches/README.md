[← Kustomize examples](../README.md)

# patches

The general escape hatch: change any field the named transformers do not cover.

```yaml
resources:
  - ../../base
patches:
- path: deployment.yaml
  target:
    kind: Deployment
    name: ubuntu
    labelSelector: "env=dev"
```

The base here has **two** `Deployment`s (`deployment.yaml` and `deployment2.yaml`), which is the
point of the example: `target` decides which of them the patch reaches.

| Target field | Matches on |
|---|---|
| `kind`, `group`, `version` | resource type |
| `name`, `namespace` | identity, and both accept regular expressions |
| `labelSelector`, `annotationSelector` | anything carrying the label or annotation |

Without `target`, the patch applies to whatever its own `apiVersion`, `kind` and `name` identify —
one resource. With it, **one patch file can apply to many resources at once**, which is how you
add a sidecar, a `securityContext` or a `nodeSelector` to everything in a base without writing a
patch per workload.

The patch file itself ([`overlays/dev/deployment.yaml`](overlays/dev/deployment.yaml)) is a
**strategic merge patch**: a partial `Deployment` containing only the fields to change — here the
container's resource requests and limits. Kustomize merges it field by field.

Two things to know about strategic merge patches:

- **Lists are merged by key, not by position.** `containers` merges on `name`, so the patch must
  repeat the container name to reach it. That is why the patch names `ubuntu` rather than
  addressing `containers[0]`.
- **The alternative is JSON Patch** (`op: replace`, `path: /spec/...`), which addresses lists by
  index. Prefer strategic merge; an index-based patch breaks silently the day someone reorders
  the base.

Rendered result in [`output.yaml`](output.yaml):

```bash
kustomize build overlays/dev -o output.yaml
```

---

[← Kustomize examples](../README.md)
