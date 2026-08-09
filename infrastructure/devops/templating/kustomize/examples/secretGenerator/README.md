[← Kustomize examples](../README.md)

# secretGenerator

The same machinery as [`configMapGenerator`](../configMapGenerator/README.md), producing
`Secret`s.

```yaml
resources:
  - ../../base
secretGenerator:
  - name: my-secret
    behavior: merge
    literals:
      - username=YW5kcmV5
      - password=YW5kcmV5
  - name: my-secret2
    behavior: create
    literals:
      - username=YW5kcmV5
      - password=YW5kcmV5
  - name: env_file_secret
    namespace: apps
    envs:
    - env.txt
    type: Opaque
    options:
      annotations:
        app_config: "true"
      labels:
        app.kubernetes.io/name: "app2"

generatorOptions:
  labels:
    fruit: apple
```

Three entries, each showing something different.

**`merge` keeps the base's name.** In [`output.yaml`](output.yaml), `my-secret` comes out as
`my-secret` — no hash — because it merges into the `Secret` that already exists in the base.
`my-secret2`, created fresh, gets `my-secret2-h4c726c75b`. Worth noticing: merging into an
existing resource does not give you the change-detection that the hash provides.

**`envs:` reads key/value pairs from a file.** `env.txt` contains `andrey=devops`, and each line
becomes one key. This is the `.env` format, and it is the right input when the values come from
somewhere else rather than being typed into the `kustomization.yaml`.

**`options:` is per-generator.** Labels and annotations set there apply to that resource only,
and stack with the `generatorOptions` block, which applies to everything. In the output,
`env_file_secret-fmch68t8kb` carries both its own `app.kubernetes.io/name: app2` and the global
`fruit: apple`.

## These are not secrets

**base64 is encoding, not encryption.** `YW5kcmV5` is `andrey` to anyone with a terminal. The
values here are committed to Git in plain sight, which is fine for an example and unacceptable
for anything real.

`secretGenerator` is still worth using — it produces the right shape and gets the name hash —
but the values have to come from somewhere that is not the repository: SOPS, Sealed Secrets, or
an operator pulling from an external store. The `envs:` form is the one that fits that, since the
file can be decrypted at build time rather than committed in the clear.

Rendered result in [`output.yaml`](output.yaml):

```bash
kustomize build overlays/dev -o output.yaml
```

---

[← Kustomize examples](../README.md)
