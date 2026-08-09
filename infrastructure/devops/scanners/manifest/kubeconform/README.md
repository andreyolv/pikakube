[← Manifest scanners](../README.md)

# kubeconform

<https://github.com/yannh/kubeconform>

Recorded example: <https://github.com/yannh/kubeconform#github-workflow>

---

## The problem it solves

A manifest can be perfectly valid YAML and still be nonsense to Kubernetes: a misspelled field, a
string where an integer belongs, an `apiVersion` removed two releases ago. [yamllint](../yamllint/README.md)
will not catch any of it, because it is all syntactically fine.

kubeconform validates manifests against the **Kubernetes OpenAPI schemas** — the actual API
definitions, per version — offline and without a cluster:

| Property | Detail |
|---|---|
| **Fast** | parallel validation; it does not add meaningful time to a pipeline |
| **Offline** | schemas can be cached or vendored; no API server required |
| **Version-targeted** | `-kubernetes-version 1.31.0` answers "will this apply on the cluster we are actually running" |
| **CRD-capable** | `-schema-location` accepts additional schema sources, which is how CRDs get validated |
| **Strict mode** | `-strict` rejects unknown fields, which is where typos are caught |

Without `-strict`, an unknown field is ignored and the manifest passes — the same behaviour the API
server has, and the reason a typo in a field name silently does nothing for months. `-strict` is
the flag that makes the tool worth running.

Version targeting is the other high-value feature: it turns "this manifest uses a deprecated API"
from a discovery made during a cluster upgrade into a build failure made months earlier.

## When to use it

- **in CI, on every manifest, always.** This is the cheapest quality gate in the discipline —
  seconds of runtime, no infrastructure, and it catches a whole class of error before it reaches a
  cluster
- before a Kubernetes upgrade, run against the **target** version to find removed APIs across the
  whole repository at once
- after rendering Helm or Kustomize output, so what is validated is what will actually be applied
- with CRD schemas configured, otherwise every custom resource is skipped and the coverage claim is
  misleading

## When not to use it

- **as the only check.** It validates structure, not sense. A Deployment with no resource requests,
  no probes and `image: latest` is schema-valid — that is [kube-score](../kube-score/README.md)
- as a substitute for policy enforcement at admission time
- on unrendered Helm templates. Go template syntax is not valid YAML; render first
- without CRD schemas, on a repository full of custom resources, while claiming everything is
  validated

## Notes

Two recorded references. The project, <https://github.com/yannh/kubeconform>, and the GitHub
workflow example in its README, <https://github.com/yannh/kubeconform#github-workflow>.

**The recorded opinion about that example is blunt**: *"exemplo de workflow fezes puríssima"* —
"the workflow example is pure garbage". It is recorded precisely because it is the first thing
anyone lands on when wiring kubeconform into CI, and following it produces a worse pipeline than
writing four lines yourself. Take the flags from it, not the structure.

kubeconform is the successor to `kubeval`, which is archived and no longer tracks current
Kubernetes schemas. Anything still using kubeval should move; the flags are close enough that it is
a small change.

Nothing is deployed for this — it is a CLI, and it belongs in a pipeline rather than in a cluster.

Its place among the four tools in [`../`](../README.md) is **the second layer**: yamllint proves it
is YAML, kubeconform proves it is Kubernetes, [kube-score](../kube-score/README.md) argues about
whether it is good Kubernetes. Running them in that order gives errors in the order they can be
understood.

---

[← Manifest scanners](../README.md)
