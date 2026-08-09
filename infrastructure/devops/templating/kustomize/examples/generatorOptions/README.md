[← Kustomize examples](../README.md)

# generatorOptions

Settings applied to **everything** the generators produce — every `ConfigMap` and every `Secret`
in the overlay.

```yaml
resources:
  - ../../base
secretGenerator:
  - name: my-secret2
    behavior: create
    literals:
      - username=YW5kcmV5
      - password=YW5kcmV5
generatorOptions:
  labels:
    kustomize.generated.resources: secret-label
  annotations:
    kustomize.generated.resource: secret-annotation
  disableNameSuffixHash: true
  immutable: true
```

| Option | Effect |
|---|---|
| `labels` | added to every generated resource |
| `annotations` | the same, for annotations |
| `disableNameSuffixHash` | stop appending the content hash to generated names |
| `immutable` | mark generated `ConfigMap`s and `Secret`s immutable |

## disableNameSuffixHash is a trade, not a tidy-up

The hash is a feature. Because a content change produces a new name, and every reference to it is
rewritten, the workload's spec changes and **the pods roll**. Turn the hash off and that stops:
the `ConfigMap` is updated in place, the `Deployment` is byte-identical, nothing restarts, and
the pods keep serving the old values until something else happens to restart them.

There are legitimate reasons to disable it — a resource referenced by something outside this
kustomization, or by name from application code. If you do, you own the restart: a checksum
annotation on the pod template, or a config-reloader sidecar.

## immutable pairs badly with it

`immutable: true` makes the resource unmodifiable after creation, which is genuinely useful — the
API server skips watching it, reducing load, and nothing can change it by accident.

But immutable plus hashed names is the coherent combination: a change produces a *new* resource
with a new name, and the old one is garbage-collected. Immutable plus `disableNameSuffixHash`
means the resource can never be changed and can never be replaced under the same name — updating
it requires deleting it first, by hand.

This example sets both. Read it as a demonstration of the options, not as a configuration to
copy.

Note also that `labels` here are applied to generated resources only, unlike
[`commonLabels`](../commonLabels/README.md), which touches every resource in the overlay.

Rendered result in [`output.yaml`](output.yaml):

```bash
kustomize build overlays/dev -o output.yaml
```

---

[← Kustomize examples](../README.md)
