[← Manifest templating](../README.md)

# Kustomize

<https://github.com/kubernetes-sigs/kustomize>

---

## The problem it solves

The same application in dev and production differs in a handful of fields — replicas, image tag,
namespace, a couple of resource limits. Copying the whole manifest set per environment means every
future change has to be made in every copy.

Kustomize solves that **without a template language**. You keep one base of ordinary, valid
Kubernetes YAML, and each overlay is a `kustomization.yaml` that patches it. Nothing in the base
is parameterised, nothing has placeholders, and every file in the tree is a document `kubectl`
would accept on its own.

Two properties follow from that and they are the whole argument for the tool:

- **It is already installed.** `kubectl apply -k` and `kubectl kustomize` are built into
  `kubectl`. No new binary, no new dependency in CI.
- **It understands the documents.** Because it parses YAML rather than concatenating strings, it
  can find a container by name, rewrite an image reference wherever it appears, and add a label
  to every resource including the selectors that have to match.

## When to use it

- **Environment deltas over one base** — the case it was designed for, and where it is clearly
  the right answer.
- **Manifests you own and only you deploy.** No packaging, no versioning, no registry needed, so a
  chart would be pure overhead.
- **On top of rendered output from something else.** Kustomize can take a chart's rendered
  manifests as a base, which is the standard escape hatch when an upstream chart does not expose
  the field you need.
- **With a GitOps controller.** Flux's `Kustomization` and Argo CD both apply Kustomize
  directories natively.

## When not to use it

- **When the variation is parameterisation, not deltas.** Kustomize has **no parameters and no
  conditionals**. Anything that varies needs its own overlay, so a matrix of services times
  environments produces an overlay tree that grows multiplicatively and reintroduces the
  duplication overlays were supposed to remove.
- **When you need to distribute it.** There is no package format, no version, no dependency
  resolution and nowhere to publish. That is [Helm](../helm/README.md).
- **When the logic is real logic** — generating a resource per item in a list, or computing
  values. Use something from the
  [programming-language family](../README.md#23-real-programming-languages).

## Notes

The recorded link is [kubernetes-sigs/kustomize](https://github.com/kubernetes-sigs/kustomize).

### Worked examples

A base-and-overlay example exists in this folder for each transformer, with the rendered result
committed as `output.yaml` next to it — so the effect of each field is visible as a diff rather
than a description. See [`examples/`](examples/README.md).

Every example was produced with the same command, recorded as a comment in each overlay:

```bash
kustomize build overlays/dev -o output.yaml
```

### Things the examples make concrete

| Behaviour | Why it matters |
|---|---|
| `commonLabels` also rewrites **selectors** | convenient, and it makes the label immutable in practice — a `Deployment`'s `spec.selector` cannot be changed after creation, so changing a common label later means deleting and recreating |
| `labels` with `includeSelectors` / `includeTemplates` | the newer, explicit form of the same thing — you choose whether selectors are touched instead of it being implied |
| generators append a **content hash** to the name | changing a `ConfigMap` produces a new name, so the `Deployment` referencing it changes too and actually rolls. `disableNameSuffixHash: true` turns that off, and turns off the rollout with it |
| `behavior: create` / `replace` / `merge` | how an overlay's generator interacts with one of the same name in the base — the source of most "why is my value not applied" confusion |
| `patches` with a `target` selector | one patch applied to every resource matching a kind, name or label, rather than named file by file |
| `secretGenerator` literals are **not encrypted** | the values in these examples are base64 strings in Git, which is encoding, not secrecy — real secrets need SOPS, Sealed Secrets or an external store |

---

[← Manifest templating](../README.md)
