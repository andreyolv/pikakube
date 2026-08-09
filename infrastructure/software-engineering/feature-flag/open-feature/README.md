[← Feature flags](../README.md)

# OpenFeature

<https://github.com/open-feature/spec>
<https://github.com/open-feature/open-feature-operator>

---

## The problem it solves

**OpenFeature is not a flag backend.** It is a specification, and the first link above being the
`spec` repository rather than a program is the whole tell.

The problem it addresses is lock-in at the call site. Every flag vendor ships an SDK with its own
API, so `unleash.isEnabled(...)` or `flagsmith.hasFeature(...)` ends up written in hundreds of
places across the codebase. Changing vendor then means touching all of them, which is why nobody
does — the decision made in week one becomes permanent by accident.

OpenFeature puts a vendor-neutral API in front:

```
application code  →  OpenFeature SDK  →  provider  →  Unleash / Flagsmith / flagd / ...
```

You call `getBooleanValue("new-checkout", false, context)`. A **provider** — a small adapter —
connects that to whichever backend you chose. Swapping backends becomes a configuration change at
one place instead of a refactor everywhere.

What comes with the standard:

| Piece | What it is |
|---|---|
| The specification | evaluation semantics, the context model, error behaviour — defined once, across languages |
| SDKs | one API per language, maintained by the project |
| Providers | adapters to specific backends, some official, some from the vendor |
| **Hooks** | logging, telemetry, validation attached around every evaluation, in one place |
| `flagd` | the project's own reference evaluation engine, usable as a backend in its own right |
| The **operator** | the Kubernetes-native deployment — see below |

It is a CNCF project, which is why "put the standard in front of the vendor" is a cheaper bet here
than it usually is: the neutral layer is not owned by one of the vendors it abstracts.

## When to use it

- **always, in application code.** The cost is one library; the benefit is that the vendor choice
  stops being irreversible
- a polyglot fleet, where the same evaluation semantics across languages is worth having
- you want telemetry on flag evaluations without instrumenting each call site — that is what hooks
  are for
- you genuinely may change backend later, or have not decided yet and want to start writing code

## When not to use it

- you expected it to **store flags**. It does not. Something still has to hold the rules, and this
  folder's other three entries are the candidates
- the provider for your language and your chosen backend is immature or missing. **Check the
  matrix rather than assuming it is filled in** — coverage varies by language and by vendor, and a
  missing provider means writing one
- a single application, one language, one backend, and a team that will not revisit it — the layer
  is then real indirection for a benefit nobody will collect

## Notes

**What is deployed here:** chart `open-feature-operator` 0.8.1 from
`https://open-feature.github.io/open-feature-operator/`, in the `open-feature` namespace, with an
empty `values` block.

**Note what that chart is.** It is the **operator**, not the SDK — the SDK is a library your
application imports and has nothing to install. The operator is a different, Kubernetes-specific
deployment model: it watches pods for an annotation and **injects `flagd` as a sidecar**, with
flag definitions supplied through custom resources. The application then evaluates against
`localhost`.

The two models are genuinely different choices:

| | **SDK plus provider** | **Operator plus `flagd` sidecar** |
|---|---|---|
| What runs | a library, in your process | a sidecar container, per pod |
| Where rules come from | the backend, via the provider | custom resources, synced by the operator |
| Language coverage | needs a provider per language | any language that can make an HTTP or gRPC call |
| Cost | none beyond the library | a container per pod, and the operator |
| Fits | an existing Unleash or Flagsmith backend | flags declared as Kubernetes resources, no separate backend |

Installing the operator is therefore closer to *choosing `flagd` as the backend* than to *adopting
the standard*. Adopting the standard costs nothing and happens in the application repositories.

**The recommendation this folder settles on:** code against the OpenFeature API regardless, and
pick exactly one backend behind it — see the [parent README](../README.md#10-how-this-applies-to-pikakube)
for which one and why. The standard is the cheap half of the decision; the backend is the half
worth thinking about.

---

[← Feature flags](../README.md)
