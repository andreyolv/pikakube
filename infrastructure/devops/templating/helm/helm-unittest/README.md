[← Helm](../README.md)

# helm-unittest

<https://github.com/helm-unittest/helm-unittest>

---

## The problem it solves

A Helm chart is a **program** that emits YAML, and it is the one program in most repositories with
no tests at all.

[`../README.md`](../README.md) sets out why Go templating is the weak part of Helm: the tool does
not understand YAML until after rendering, so a whitespace bug, a wrong `{{- if }}` or a value that
falls through to the wrong default produces output that is syntactically fine and semantically
wrong. Nobody notices, because nobody renders the chart with that particular combination of values
until the day it matters.

helm-unittest is a Helm plugin that asserts on **rendered output**, per test case, with its own set
of values:

```yaml
suite: deployment
templates:
  - deployment.yaml
tests:
  - it: sets replicas from values
    set:
      replicaCount: 3
    asserts:
      - equal:
          path: spec.replicas
          value: 3

  - it: has no resource limits by default
    asserts:
      - isNull:
          path: spec.template.spec.containers[0].resources.limits
```

The second test is the interesting shape: it pins a **default**. Defaults are where charts break
silently, because changing one is invisible in a diff of the template.

## What it actually catches

| Failure | Why nothing else sees it |
|---|---|
| **A conditional branch never rendered** | `{{- if .Values.x }}` with `x` unset in the only values file anyone tries |
| **A default that changed** | the template still renders; the output is different |
| Indentation from `nindent`/`toYaml` | valid YAML, wrong nesting, wrong object |
| A value that does not reach the template | typo in the path; the template falls back silently |
| Output differing per values combination | nobody renders all of them by hand |
| A removed field | the chart renders fine and the workload loses a setting |

The first row is the one that justifies the tool. A chart with six feature flags has sixty-four
rendering paths, and CI usually exercises one.

## When to use it

- **you author or fork Helm charts** — this is the case it exists for
- a chart has conditionals, and therefore combinations nobody renders by hand
- an internal chart is consumed by other teams, so its defaults are a contract
- refactoring a chart's templates and needing to prove the output did not change

## When not to use it

- **you only consume upstream charts**, which is most platforms — you are not the one who can fix a
  bug it finds
- the requirement is "does this manifest make sense to Kubernetes" — that is
  [flux-schema](../../../scanners/manifest/flux-schema/README.md) or
  [kubeconform](../../../scanners/manifest/kubeconform/README.md), on the rendered output
- the requirement is policy — [conftest](../../../../security/2-cluster/policies/conftest/README.md)
  or [Kyverno](../../../../security/2-cluster/policies/kyverno/README.md)
- as a substitute for actually installing the chart somewhere; rendering correctly and working are
  different claims

## Where it sits among the checks

Four things can be done to a chart, and they are not alternatives:

| Question | Tool |
|---|---|
| Does the template render at all? | `helm template`, or `helm lint` |
| **Does it render the right thing, for these values?** | **helm-unittest** |
| Is the rendered output valid Kubernetes? | [flux-schema](../../../scanners/manifest/flux-schema/README.md) / [kubeconform](../../../scanners/manifest/kubeconform/README.md) |
| Is it *good* Kubernetes, and does it meet policy? | [kube-score](../../../scanners/manifest/kube-score/README.md), [conftest](../../../../security/2-cluster/policies/conftest/README.md) |

Only the second is about the chart as a program. The rest are about its output, and they would say
the same thing about a hand-written manifest.

## Notes

Added to the catalogue from <https://github.com/helm-unittest/helm-unittest>. Installed as a Helm
plugin (`helm plugin install`), MIT licensed, with tests as YAML files under the chart's `tests/`
directory. Note the project moved to the `helm-unittest` organisation from its original home —
older references point at the previous path.

**The honest position for pikakube:** this repository **consumes** charts rather than authoring
them. Nearly every deployment here is a `HelmRelease` pointing at an upstream chart, so there is no
chart of ours whose templates could be unit-tested.

That makes it the least immediately applicable of the tools in this folder, and it is worth
cataloguing for two reasons.

**It names a real gap in the ecosystem.** The recurring finding across this whole repository is
charts that do not work —
[DataHub's chart *"never works"*](../../../../data-governance/platform/datahub/README.md),
[Amundsen's is broken](../../../../data-governance/catalog/amundsen/README.md),
[ThreatMapper's `HelmRelease` has no name or version](../../../../security/0-governance/cnapp/threatmapper/README.md),
[Kubewarden's two releases collide](../../../../security/2-cluster/policies/kubewarden/README.md).
Those are chart-authoring failures, and this is the class of tool that would have caught several of
them.

**It becomes relevant the moment a chart is written here.** Several components in this tree are
deployed from hand-written manifests that would be better as a small internal chart — at which point
its defaults become a contract with whoever consumes it, and untested defaults are how that contract
breaks quietly.

---

[← Helm](../README.md)
