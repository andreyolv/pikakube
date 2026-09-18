[← Evaluation](../README.md)

# promptfoo

<https://github.com/promptfoo/promptfoo>

---

## The problem it solves

promptfoo is the CI-shaped answer to [`evaluation/`](../README.md) section 2's first row. Test cases
are declared in a YAML file beside the prompt: inputs, the providers to run them against, and
assertions — exact match, regex, JSON schema, embedding similarity, or a model-graded rubric where
the check genuinely needs judgement.

Two properties make it the usual starting point:

- **It runs from the command line and exits non-zero.** That makes it a pipeline step like any
  other, which is the difference between evaluation as a habit and evaluation as an exercise
  somebody did once in a notebook.
- **Every case runs against every provider.** One config, several models or several prompt
  versions, results side by side. That is how "should we move to the cheaper model" stops being an
  argument about intuitions.

It also has a `redteam` mode that generates adversarial cases — jailbreaks, injection, PII
extraction. Useful, and it answers the *different* question in section 2: whether the thing can be
made to misbehave, not whether it is any good.

The web UI — what is deployed here — reads the results of those runs. It is the smaller half of the
tool.

## When to use it

- prompts or model choices change and nobody currently knows whether quality moved
- a model migration needs evidence rather than a hunch
- the assertions are mostly mechanical — schema, contains, refuses-when-it-should — with a few
  model-graded ones
- evaluation should live next to the code, in the same repository and review

## When not to use it

- there is no task to evaluate yet. The tool is trivial; the dataset is the work, and it cannot be
  started before there is something being asked of a model
- evaluation belongs inside a Python test suite in a unit-test idiom — `deepeval` fits that shape
  better
- tracing and online evaluation of production traffic is what is actually needed — that is
  [Langfuse](../../agents/langfuse/README.md), and the two are complementary rather than
  alternatives

## Notes

- <https://www.promptfoo.dev/docs/> — the documentation, including the assertion reference, which is
  the page to read first: what can be checked deterministically decides how much of the eval set
  needs a judge model at all.

### Why this is a GitRepository and not an OCIRepository

promptfoo **does not publish its Helm chart**. There is no OCI artefact, no Helm repository, and
nothing on Artifact Hub — the chart exists only as `helm/chart/promptfoo` inside the application
repository. So the source here is a Flux `GitRepository` pinned to tag `0.123.0` with a
`sparseCheckout` on that one path, and the `HelmRelease` references it by chart path.

The cost of that is worth stating plainly: **Renovate does not see this file.** The repository's
[`renovate.json5`](../../../../.github/renovate.json5) restricts the Flux manager to files named
`ocirepository.yaml`, so both the Git tag and the image tag below are updated by hand. If upstream
ever publishes the chart, this becomes an ordinary `ocirepository.yaml` and rejoins the grouped
update pull request.

### The values, and why each override exists

The upstream chart is unmaintained relative to the application — `version: 0.1.0`, `appVersion:
0.54.1`, while the released image is on 0.123.x. Three of its defaults do not work as shipped:

| Default | Problem | Override |
|---|---|---|
| `image.tag: v1.0.0` | that tag does not exist in the registry | pinned to `0.123.0` |
| `imagePullSecrets: [name: <yourcred>]` | a placeholder secret name; the image is public | emptied |
| `nodeSelector: kubernetes.io/arch: amd64` | will not schedule on arm64 nodes | `null` |

The `nodeSelector` override is `null` and not `{}` on purpose: Helm **merges** maps, so an empty map
leaves the upstream key exactly where it was. `helm template` with `{}` still renders
`kubernetes.io/arch: amd64`. Lists are replaced wholesale, which is why `imagePullSecrets: []` does
work.

`persistentVolumesClaims` keeps the 1Gi volume mounted at `/home/promptfoo/.promptfoo`, which is
where the results database lives — without it, every restart loses the history the UI exists to
show. `storageClassName: standard` is the Kind default and is the value to change on a real
cluster.

One defect cannot be worked around from values at all: **the chart renders an `Ingress`
unconditionally**, with `ingressClassName: traefik` and `cert-manager.io/cluster-issuer:
letsencrypt-cloudflare` written into the template rather than taken from a value. There is no
`ingress.enabled`. This platform runs [NGINX](../../../network/ingress-controller/README.md) and
[mkcert](../../../security/2-cluster/certificates/mkcert/README.md), so that object will sit there
unclaimed by any controller. Only the host is a value, so it is set to a `nip.io` name for
consistency with the rest of the repository; reaching the UI is a `kubectl port-forward` on service
port 3000.

### What this deployment is, and is not

It is the **viewer**. The evaluations themselves run wherever the config file is — a developer's
machine or a CI job — and the useful next step is a `promptfooconfig.yaml` in this repository
pointed at something actually deployed, rather than a larger install. Nothing in
[`ai/`](../../README.md) has a defined task yet, which is the honest blocker and not a tooling gap.

---

[← Evaluation](../README.md)
