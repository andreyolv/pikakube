[← Kustomize](../README.md)

# Kustomize examples

One folder per transformer, each with a `base/`, an `overlays/dev/`, and the rendered
`output.yaml` committed next to them so the effect is readable as a diff.

Every one was produced the same way, from inside the example folder:

```bash
kustomize build overlays/dev -o output.yaml
```

The base is the same throughout — an `ubuntu` `Deployment` that sleeps, plus a `Secret` — so the
only thing that differs between examples is the field being demonstrated.

| Example | Field | What it shows |
|---|---|---|
| [`namespace`](namespace/README.md) | `namespace:` | rewrites the namespace of every resource, overriding what the base declares |
| [`namePrefix`](namePrefix/README.md) | `namePrefix:` | prefixes every resource name, and fixes up references to them |
| [`nameSuffix`](nameSuffix/README.md) | `nameSuffix:` | the same, appended |
| [`commonLabels`](commonLabels/README.md) | `commonLabels:` | labels on every resource **including selectors and pod templates** |
| [`labels`](labels/README.md) | `labels:` with `includeSelectors` / `includeTemplates` | the explicit replacement for `commonLabels` — you choose whether selectors are touched |
| [`commonAnnotations`](commonAnnotations/README.md) | `commonAnnotations:` | annotations on every resource; unlike labels, never part of a selector, so always safe |
| [`image`](image/README.md) | `images:` | swap `newName` and `newTag` wherever the image appears, without patching each container |
| [`replicas`](replicas/README.md) | `replicas:` | replica count by resource name — the one field that differs per environment more than any other |
| [`patches`](patches/README.md) | `patches:` with `target:` | a patch applied by kind, name and label selector rather than to one named file |
| [`configMapGenerator`](configMapGenerator/README.md) | `configMapGenerator:` | `ConfigMap`s from literals and from files, with `behavior:` controlling merge against the base |
| [`secretGenerator`](secretGenerator/README.md) | `secretGenerator:` | the same for `Secret`s, including `envs:` reading key/value pairs from a file |
| [`generatorOptions`](generatorOptions/README.md) | `generatorOptions:` | labels, annotations, `immutable`, and `disableNameSuffixHash` applied to everything generated |

## The three that surprise people

**`commonLabels` rewrites selectors.** That is usually what you want, and it has a consequence: a
`Deployment`'s `spec.selector` is immutable after creation, so changing a common label later
fails on apply and requires deleting the resource. The newer `labels:` form exists so that
`includeSelectors` is a decision rather than a default — see the
[`labels`](labels/README.md) example next to the [`commonLabels`](commonLabels/README.md) one.

**Generators append a content hash to the name.** `my-config-map` becomes
`my-config-map-<hash>`, and every reference to it is rewritten. This is the mechanism that makes
a config change actually roll the pods, because the `Deployment` now points at a different name.
`disableNameSuffixHash: true` — used in the [`generatorOptions`](generatorOptions/README.md)
example — removes it, and removes the automatic rollout too. Turn it off deliberately, not by
habit.

**`behavior:` decides what an overlay generator does to a base one of the same name.**
`create` adds a new resource, `replace` discards the base's content entirely, `merge` combines
them. The [`configMapGenerator`](configMapGenerator/README.md) example uses all three side by
side, which is the quickest way to see why a value seems to have been ignored.

## A note on the secrets

The literals in [`secretGenerator`](secretGenerator/README.md) and
[`generatorOptions`](generatorOptions/README.md) are base64 strings committed to Git. **base64 is
encoding, not encryption.** These are demonstration values; anything real needs SOPS, Sealed
Secrets or an external secret store.

---

[← Kustomize](../README.md)
