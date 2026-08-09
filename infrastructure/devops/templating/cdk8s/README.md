[← Manifest templating](../README.md)

# cdk8s

<https://github.com/cdk8s-team/cdk8s>

---

## The problem it solves

Templating languages are programming languages that nobody chose and nobody enjoys. Go templates
have no types, no debugger and no editor support; a typo in a field name renders happily and is
rejected by the API server.

cdk8s inverts that: **write the configuration in a real language** — TypeScript, Python, Java or
Go — and synthesise YAML from it. The Kubernetes API is a set of generated classes, so the
editor autocompletes `spec.template.spec.containers`, the compiler rejects a misspelled field,
and shared behaviour is a function rather than a copied block.

The other half is **constructs**: composable objects at whatever level of abstraction you want.
A `WebService` construct emits a `Deployment`, a `Service`, an `Ingress` and a
`PodDisruptionBudget`, and is used in one line. The model comes from AWS CDK, which is the same
team's earlier work.

The output is plain YAML applied with `kubectl` or reconciled by a GitOps controller — cdk8s runs
at build time and nothing about it exists in the cluster.

## When to use it

- **The team already writes TypeScript or Python.** The whole value proposition is using a
  language people already know well; adopting one just for this defeats it.
- **Lots of structural repetition** — many similar services where the difference is genuinely
  computed, not just a few field values.
- **Abstractions with real behaviour**, where "our standard service" means a set of resources
  with rules between them rather than a values file.

## When not to use it

- **Configuration a mixed audience has to read.** YAML is legible to everyone who runs the
  cluster; TypeScript is legible to the people who write TypeScript. That is a narrower group,
  and it includes whoever is on call at 3am.
- **Consuming third-party software.** Nobody publishes cdk8s constructs for their product; they
  publish [Helm charts](../helm/README.md).
- **When the diff has to be reviewable.** The commit changes source code, and what changed in the
  cluster is only visible after synthesising. That is a real cost in a GitOps workflow, and the
  usual mitigation — committing the synthesised YAML too — means two things to keep in sync.

## Notes

The recorded link is [cdk8s-team/cdk8s](https://github.com/cdk8s-team/cdk8s).

cdk8s is a CNCF project and the most credible member of the
[real-language family](../README.md#23-real-programming-languages) for teams with an existing
TypeScript or Python codebase, because there is no new language to learn — only a library.

`cdk8s+` is worth naming separately: it is the higher-level API on top of the generated
Kubernetes types, where `new kplus.Deployment(...)` fills in the defaults that the raw API
requires you to spell out. The generated low-level API mirrors the Kubernetes API exactly and is
verbose for the same reason the Kubernetes API is.

It also imports CRDs — pointing it at a CRD schema generates typed classes for it — which is the
one place where types buy something no amount of YAML review does: custom resources have no
client-side validation until they reach the API server.

For this repository it is an alternative on the list, not a candidate. Everything here is applied
as a Flux `HelmRelease` or `Kustomization`, and a synthesis step before that adds a build to a
pipeline that currently has none.

---

[← Manifest templating](../README.md)
