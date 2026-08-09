[← Kustomize examples](../README.md)

# nameSuffix

The same mechanism as [`namePrefix`](../namePrefix/README.md), appended instead of prepended.

```yaml
resources:
  - ../../base
nameSuffix: -dev
```

`ubuntu` becomes `ubuntu-dev`. References to renamed resources are rewritten the same way.

Prefix or suffix is a naming-convention choice, not a functional one. Suffixes sort names by
application, prefixes sort them by environment — pick one and be consistent, because mixing them
across a repository makes `kubectl get` output unreadable.

Both can be applied at once, and both stack when overlays are nested, which is worth remembering
before building a three-level overlay tree.

Rendered result in [`output.yaml`](output.yaml):

```bash
kustomize build overlays/dev -o output.yaml
```

---

[← Kustomize examples](../README.md)
