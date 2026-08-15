[← GitHub Actions](../README.md)

# setup-helm

<https://github.com/Azure/setup-helm>

Marketplace: *Helm tool installer*

---

## The problem it solves

The same problem as [setup-kubectl](../setup-kubectl/README.md), for the other binary in the pair:
a job that needs `helm` either takes whatever the runner image happens to ship, curls the installer
script and gets whatever is current that morning, or declares the version it wants in one line.

```yaml
- uses: azure/setup-helm@<commit-sha>   # not @v4
  with:
    version: v3.16.3
```

It downloads a named Helm release, puts it on the runner's `PATH`, and outputs the path it installed
to. MIT-licensed, maintained by Microsoft/Azure, and — like its sibling — **explicitly outside the
Azure support policy**. It looks first-party and is not `actions/`.

The `version` input accepts a semantic version, `latest`, or a version constraint. As with
`setup-kubectl`, **the default is `latest` and the default is the wrong choice** — see
[notes](#notes).

## The question to answer before adding it

**What does the job do with Helm?** Helm is two tools wearing one name, and the answer decides
whether this action is a build dependency or a deployment credential in disguise.

| What the step runs | Verdict |
|---|---|
| `helm template`, `helm lint`, `helm dependency build` — rendering and checking a chart locally | fine — Helm as a **templating tool**, no cluster involved |
| `helm package` + `helm push` to an OCI registry | fine, and genuinely useful — this is chart *publishing*, which is CI's job |
| `helm show values` / `helm search` against a repository | fine — read-only, no cluster |
| **`helm upgrade --install` against a cluster** | **stop.** This is the `kubectl apply` anti-pattern wearing a chart |

The last row is the one to look for. `helm upgrade --install` in CI needs a kubeconfig with write
access to the cluster, which inverts the direction this platform is built around: CI ends at *push
an artefact and open a pull request*, and [Flux](../../../../platform-engineering/gitops/flux/README.md)
pulls from there via `HelmRelease`. See [CI/CD §3](../../README.md#3-the-credentials-consequence)
and [GitHub Actions §8](../README.md#8-anti-patterns).

The *publishing* row is the interesting one, because it is the case where Helm in CI fits this
repository's model exactly rather than fighting it. A workflow that packages a chart and pushes it
to `ghcr.io` produces an OCI artefact; the cluster consumes it through an `OCIRepository` +
`HelmRelease` pair with a pinned tag **and digest**. That is precisely the shape of the
[falco-operator](../../../../security/2-cluster/runtime-security/falco-operator/README.md)
deployment here. CI writes the artefact, Flux decides when it lands, and no cluster credential ever
leaves the cluster.

## When to use it

- **chart CI** — `helm lint`, `helm template`, and rendering the output into
  [kubeconform](../../../scanners/manifest/kubeconform/README.md),
  [kube-score](../../../scanners/manifest/kube-score/README.md) or
  [Checkov](../../../../security/1-cloud/iac/checkov/README.md), which is the pipeline every chart
  repository should have and most do not
- **chart publishing** — `helm package` and `helm push` to an OCI registry, as described above
- **`helm unittest` / chart tests**, where a pinned Helm is the difference between a reproducible
  suite and one that changes behaviour under you
- when the job needs a **specific** Helm — a chart using a feature added in a recent minor, or one
  that must be rendered with the same version the cluster's helm-controller uses
- on [self-hosted runners](../actions-runner-controller/README.md), where the image is yours and may
  ship no Helm at all

## When not to use it

- **to deploy.** Covered above; the deployment path here is Flux, and `helm upgrade` from a pipeline
  is the exact credential decision this repository avoids
- with **`version: latest`** — Helm's own releases have changed template rendering behaviour between
  minors, and a chart that renders differently with no diff behind it is an unpleasant afternoon
- when the runner image already ships the Helm you want and you have **confirmed** it. Hosted runner
  images include Helm; the trade is one fewer fetch against drift the next time the image is rebuilt
- as a general toolchain mechanism. Five `setup-*` steps is a second declaration of the toolchain
  alongside the repository's own — see
  [toolchain §5.2](../../../../software-engineering/developer-environment/toolchain/README.md#52-ci),
  and [arkade](../../../../software-engineering/developer-environment/toolchain/arkade/README.md)
  for the one-line alternative
- to render a chart and then **commit** the output. Rendered manifests in Git is a real pattern with
  real advantages, but it is a deliberate architecture, not a side effect of a CI step

## Notes

**Pin to a commit SHA, not `@v4`.** `Azure` is not `actions`; by the rule in the
[anti-pattern table](../README.md#8-anti-patterns) this is a third-party action, tags are mutable,
and this is the class of thing [zizmor](../../../../security/4-code/pipeline/zizmor/README.md)
flags. Pair the pin with [Renovate](../../../../security/4-code/dependency/renovate/README.md) or
[Dependabot](../../../../security/4-code/dependency/dependabot/README.md), otherwise the pin becomes
a two-year-old action nobody dares touch.

**`helm template` in CI is not what the cluster will run.** This is the trap specific to Helm rather
than to the action. Rendering locally uses the values *you* pass; the cluster renders with the values
in the `HelmRelease`, a different Helm version, and — for anything using `.Capabilities` or lookup
functions — a different cluster. A chart that lints clean in CI can still produce something else in
the cluster. Render with the same values file the release uses, or accept that the check is weaker
than it looks. The same caveat is recorded for Helm scanning in
[Checkov's notes](../../../../security/1-cloud/iac/checkov/README.md#notes).

**It does not verify what it downloads.** Helm publishes checksums and provenance for its releases;
this action fetches the binary and checks neither. Same accepted risk, same escalation path as
`setup-kubectl` — see [`security/0-governance/supply-chain/`](../../../../security/0-governance/supply-chain/README.md).

**Chart provenance is a separate question the action does not touch.** `helm push` publishes; it
does not sign. If chart integrity matters, that is `cosign` over the OCI artefact and a verification
policy in the cluster — the same loose end recorded as *signing is written and commented out* in
[`workflows/`](../workflows/README.md).

**Where this fits in pikakube.** Helm here is consumed, not produced: roughly every deployed
component is a `HelmRelease` reconciled by Flux, and no chart in this repository is packaged or
published. The realistic use for this action is therefore the validation gap named in
[manifest scanners §8](../../../scanners/manifest/README.md#8-how-this-applies-to-pikakube) — a
workflow that renders the charts this repository *consumes* and checks the result before the values
change reaches a cluster. That job needs Helm and no credential at all, which is the shape to aim
for.

---

[← GitHub Actions](../README.md)
