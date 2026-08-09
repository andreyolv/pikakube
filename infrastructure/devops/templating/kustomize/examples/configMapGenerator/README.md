[← Kustomize examples](../README.md)

# configMapGenerator

Builds `ConfigMap`s from literals and from files, instead of writing the YAML by hand.

```yaml
resources:
  - ../../base
configMapGenerator:
  - name: my-config-map
    behavior: replace
    literals:
      - MY_ENV=dev
  - name: my-config-map2
    behavior: create
    literals:
      - MY_ENV=dev
  - name: andrey
    behavior: create
    files:
    - application.properties

generatorOptions:
  labels:
    fruit: apple
```

Three generators, chosen to show the three behaviours side by side. The base already contains a
`configmap.yaml`, so `behavior:` decides how the overlay's entry interacts with it.

| `behavior` | Effect on a same-named resource from the base |
|---|---|
| `create` | there is no base resource — this is a new one. The default |
| `replace` | discard the base's data entirely and use only what is declared here |
| `merge` | combine, with the overlay's keys winning |

Getting this wrong is the single most common source of "my value is not being applied": `merge`
where `replace` was meant leaves a stale key from the base, and `create` against an existing name
is an error.

## Files, not just literals

`files: [application.properties]` reads the file and makes its **filename** the key and its
**contents** the value. That is how a whole configuration file gets mounted into a container
without being pasted into YAML with the indentation hand-adjusted — the file stays a real file in
the repository, lintable and diffable on its own.

## The name hash

The generated names carry a content hash — `my-config-map2-<hash>`. Every reference to the
`ConfigMap` is rewritten to match, so **changing the content changes the `Deployment`, and the
pods actually restart**. Without this, editing a `ConfigMap` changes nothing until someone
notices the pods are still running the old values.

`disableNameSuffixHash` turns it off; see [`generatorOptions`](../generatorOptions/README.md) for
what that costs.

`generatorOptions` here adds `fruit: apple` to everything generated — both `ConfigMap`s and
`Secret`s, not only the ones in this block.

Rendered result in [`output.yaml`](output.yaml):

```bash
kustomize build overlays/dev -o output.yaml
```

---

[← Kustomize examples](../README.md)
