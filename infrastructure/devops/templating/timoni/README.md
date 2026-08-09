[← Manifest templating](../README.md)

# Timoni

<https://github.com/stefanprodan/timoni>

---

## The problem it solves

Timoni is an explicit answer to the question "what would Helm look like if it were designed
now?". It keeps everything Helm gets right — a package format, a registry, release state,
lifecycle — and replaces the Go templates with **CUE**.

CUE is a configuration language where types and values are the same thing, and combining two
configurations is *unification*: the result must satisfy both, or it is an error. That gives
schema validation, defaults and constraints in one mechanism, and it means an invalid
combination of module values fails at build time with a precise message instead of producing
YAML the API server will reject.

The rest of the model:

| Piece | Timoni | Helm equivalent |
|---|---|---|
| Package | **module**, written in CUE | chart, written in Go templates |
| Distribution | **OCI registry only** | repository or OCI |
| Instance state | stored in the cluster | stored in the cluster |
| Validation | CUE schema, before apply | `values.schema.json`, optional |
| Apply | server-side apply, with drift correction | client-side three-way merge |

Server-side apply is the quieter improvement: field ownership is tracked by the API server, so
Timoni knows what it owns and what something else changed.

## When to use it

- **Authoring modules you distribute**, where typed values and real validation are worth learning
  a language for.
- **When you have already been burned by Helm templating** — the untested values branch that
  rendered invalid YAML in production is precisely what CUE unification prevents.
- **In a Flux estate.** Timoni is written by Stefan Prodan, a Flux maintainer, and the design
  assumptions match: OCI distribution, server-side apply, drift correction.

## When not to use it

- **For third-party software.** There is no ecosystem of Timoni modules. Everything real ships as
  a chart, so Helm stays in the picture regardless.
- **When CUE is a cost you cannot justify.** It is a genuinely different way of thinking about
  configuration, unfamiliar to almost everyone, and there is no way to adopt Timoni without it.
- **When the estate is small.** The validation argument is strongest where a mistake is expensive
  and the configuration surface is large.

## Notes

The recorded link is [stefanprodan/timoni](https://github.com/stefanprodan/timoni).

The author being a Flux maintainer is worth noting rather than glossing over: it explains why the
tool assumes OCI distribution and server-side apply, and why its conventions line up with the
GitOps stack in [`platform-engineering/gitops/`](../../../platform-engineering/gitops/README.md).

Timoni's honest position is that it is **the best-designed Helm alternative and the one least
likely to displace Helm**, for a reason that has nothing to do with its design: Helm's value is
the ecosystem, and an ecosystem cannot be out-engineered. A module format with no modules solves
the half of the problem that was never the hard half.

Where it shares ground with [KCL](../kcl/README.md) — typed configuration, validated before
apply — it is worth taking seriously as a way of writing your *own* packages. As a replacement
for installing upstream charts, it is not a candidate.

---

[← Manifest templating](../README.md)
