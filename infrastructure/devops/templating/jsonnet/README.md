[← Manifest templating](../README.md)

# Jsonnet

<https://github.com/grafana/tanka>

<https://github.com/google/jsonnet>

---

## The problem it solves

Jsonnet is a data templating language: **JSON plus variables, functions, imports, conditionals
and object inheritance**. It was built at Google for exactly this problem — enormous volumes of
near-identical configuration — and it predates Kubernetes.

The distinguishing feature is the **merge operator**, `+`. Objects compose by deep merge, so a
base object and a set of overrides combine into a new object without either being mutated. That
makes environment overlays a language construct rather than a tool feature, and it composes to
any depth.

Because a Jsonnet program evaluates to JSON, and YAML is a superset of JSON, the output is
directly applicable. The language is hermetic — no I/O, no clock, no network — so the same input
always produces the same output.

**Tanka** is the deployment layer on top. Jsonnet alone evaluates to data; Tanka turns a Jsonnet
directory into environments with a target cluster and namespace, and provides `tk diff` and
`tk apply` against a live cluster. In practice "using Jsonnet for Kubernetes" means using Tanka.

## When to use it

- **Large, highly repetitive estates** — dozens of environments or clusters where the
  configuration is genuinely generated from data.
- **Inside the Grafana ecosystem.** The monitoring-mixin format, `kube-prometheus` and Grafana's
  own infrastructure are Jsonnet, and consuming those libraries means writing Jsonnet.
- **When deep merge is the operation you actually want.** No other tool here makes composing
  configuration objects this direct.

## When not to use it

- **Small setups.** The setup cost — a language, a package manager (`jsonnet-bundler`), a
  deployment tool — is fixed and does not shrink with the problem.
- **When people have to read it.** Jsonnet is terse and unfamiliar, editor support is thin, and a
  deeply merged object is hard to trace back to where a field was set. Debugging a merge chain is
  the recurring complaint.
- **When newer options fit.** [KCL](../kcl/README.md) and [Timoni](../timoni/README.md) address
  the same need with schemas and validation, which Jsonnet does not have.

## Notes

The recorded link is [grafana/tanka](https://github.com/grafana/tanka) — Grafana's Jsonnet
deployment tool, not the language itself. That is the right pointer: Tanka is what makes Jsonnet
usable for Kubernetes, by adding environments, a diff against the live cluster, and an apply.
The language lives at [google/jsonnet](https://github.com/google/jsonnet).

Jsonnet is the **oldest** approach in this folder and the reason the whole
[real-language category](../README.md#23-real-programming-languages) exists — it was solving
configuration generation before Helm was written.

Its practical relevance today is mostly the ecosystem it carries. The monitoring mixins —
prepackaged Prometheus rules and Grafana dashboards for common components — are distributed as
Jsonnet libraries, so anyone assembling observability from those is reading Jsonnet whether or not
they chose it.

For this repository it is documented as an alternative. The deployment path here is Flux, and
Tanka's model of applying from a workstation or CI is a different one.

---

[← Manifest templating](../README.md)
