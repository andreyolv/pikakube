[← GitHub Actions](../README.md)

# setup-kubectl

<https://github.com/Azure/setup-kubectl>

Marketplace: *Kubectl tool installer*

---

## The problem it solves

A workflow that needs `kubectl` has three options, and two of them are bad:

| Option | Problem |
|---|---|
| Use whatever the runner image ships | it is [preinstalled and unpinned](https://github.com/actions/runner-images) — the version moves when GitHub rebuilds the image, with no commit on your side |
| `curl -LO https://dl.k8s.io/release/$(curl -s .../stable.txt)/bin/linux/amd64/kubectl` | resolves to `latest` on the day it runs, hard-codes `linux/amd64`, and verifies nothing |
| **`uses: azure/setup-kubectl@<sha>` with `version:`** | one line, one declared version |

That is the whole of it. `setup-kubectl` downloads a named `kubectl` release, puts it on the runner's
`PATH`, and outputs the path it installed to. It is MIT-licensed, maintained by Microsoft/Azure, and
explicitly **not covered by the Azure support policy** — which is worth knowing, because it looks
first-party and is not `actions/`.

The `version` input takes `latest` or a semantic version such as `v1.30.2`. **The default is
`latest`, and the default is the wrong choice** — see [notes](#notes).

```yaml
- uses: azure/setup-kubectl@<commit-sha>   # not @v4
  with:
    version: v1.33.0
```

## The question to answer before adding it

**Why does this job need `kubectl` at all?** The answer decides whether this action is a convenience
or a warning sign, and the two cases look identical in a diff.

| Reason | Verdict |
|---|---|
| `kubectl kustomize`, `kubectl explain`, rendering or validating manifests **with no cluster** | fine — it is being used as a local YAML tool |
| Piping manifests into [kubeconform](../../../scanners/manifest/kubeconform/README.md) or [kube-score](../../../scanners/manifest/kube-score/README.md) | fine — same reason |
| Reading cluster state for a report, a smoke check, or a status comment | acceptable, with a **read-only** credential and a narrow scope |
| **`kubectl apply` at the end of the pipeline** | **stop.** This is the anti-pattern named in [GitHub Actions §8](../README.md#8-anti-patterns) and argued in [CI/CD §3](../../README.md#3-the-credentials-consequence) |

The last row is the one that matters. Installing `kubectl` in CI is harmless; **handing CI a
kubeconfig that can write to a cluster is not.** It inverts the direction this platform is built
around — CI ends at *push an image and open a pull request that updates the tag*, and
[Flux](../../../../platform-engineering/gitops/README.md) pulls from there. A workflow with cluster
admin is a credential outside the cluster, reachable by anyone who can merge a change to a workflow
file.

So: a `setup-kubectl` step is not itself a problem. It is a reliable **place to look** for one, and
the thing to read is the step after it.

## When to use it

- a workflow that needs `kubectl` as a **client-side YAML tool** — `kubectl kustomize`,
  `kubectl explain`, `kubectl create --dry-run=client -o yaml` — and touches no cluster
- **manifest validation pipelines**, where `kubectl` is one link in a chain with
  [yamllint](../../../scanners/manifest/yamllint/README.md),
  [kubeconform](../../../scanners/manifest/kubeconform/README.md) and
  [kube-score](../../../scanners/manifest/kube-score/README.md)
- **read-only cluster queries** from a job holding a scoped, short-lived credential — a drift report,
  a post-deploy check, a comment on a pull request
- when you need a **specific** `kubectl`, because the runner image's version is wrong for the cluster
  you talk to — the version-skew rule is ±1 minor from the API server, and the runner image does not
  know which cluster you meant
- on [self-hosted runners](../actions-runner-controller/README.md), where the image is yours and may
  not ship `kubectl` at all

## When not to use it

- **to deploy.** Covered above and worth repeating: this repository's deployment path is Flux, not a
  pipeline with a kubeconfig
- when the runner image's preinstalled `kubectl` is already the version you want and you have
  confirmed it. One fewer network fetch per job is real, and so is the drift the moment the image is
  rebuilt — decide which you care about rather than defaulting
- **with `version: latest`.** That is `latest` in CI, which is how a green pipeline turns red with no
  change to blame
- as a general toolchain mechanism. If the job needs five tools, five `setup-*` actions is a second
  parallel declaration of the toolchain — see
  [toolchain §5.2](../../../../software-engineering/developer-environment/toolchain/README.md#52-ci).
  The alternatives are [arkade](../../../../software-engineering/developer-environment/toolchain/arkade/README.md)
  for one readable line, or activating the repository's own environment file in CI, which is the
  answer that actually closes the laptop/CI gap
- on a job that runs fork-authored code and also holds a credential — that is a different problem
  and this action does not change it

## Notes

**Pin the action to a commit SHA, not to `@v4`.** This is a third-party action by the letter of the
rule — the organisation is `Azure`, not `actions` — and a tag is mutable. `@v4` means "whatever that
tag points at when the job runs", which is arbitrary code in a job that may hold credentials. It is
the first row of the [anti-pattern table](../README.md#8-anti-patterns) and the exact class of thing
[zizmor](../../../../security/4-code/pipeline/zizmor/README.md) flags. Keeping SHAs current is what
[Renovate](../../../../security/4-code/dependency/renovate/README.md) or
[Dependabot](../../../../security/4-code/dependency/dependabot/README.md) is for; pinning without an
updater is how a workflow ends up on a two-year-old action.

**`version: latest` deserves its own line because it is the default.** Omitting the input is not
neutral — it opts into a moving target. Two runs of the same commit, weeks apart, get different
binaries, and the day a `kubectl` release changes an output format or drops a deprecated flag, the
failure has no diff behind it. Pin the version, and pin it to something compatible with the cluster
the job talks to.

**It does not verify what it downloads.** Kubernetes publishes a checksum, a Sigstore signature and
a certificate for every release binary — see
[downloadkubernetes](../../../../software-engineering/developer-environment/toolchain/downloadkubernetes/README.md)
for the mechanics — and this action fetches the binary without checking any of them. For most
pipelines that is an accepted risk. For a pipeline that produces an artefact you ship, it is one of
the gaps [`security/0-governance/supply-chain/`](../../../../security/0-governance/supply-chain/README.md)
exists to close, and the fix is a verification step rather than a different action.

**Its siblings.** Azure publishes the same shape for the rest of the Kubernetes client set —
`azure/setup-helm`, `azure/setup-kubectl`, `azure/k8s-set-context`, `azure/aks-set-context`. The
first two are ordinary tool installers with the same caveats as this one. **The context actions are a
different category entirely**: their job is to put a kubeconfig on the runner, which is precisely the
credential decision this page argues against making casually. Installing a binary and granting
cluster access get written on adjacent lines and should not be waved through together.

**Where this fits in pikakube.** No workflow here installs `kubectl` today, and the direction
recorded in [GitHub Actions §10](../README.md#10-how-this-applies-to-pikakube) is that CI does not
deploy. The realistic use is the gap named in
[manifest scanners §8](../../../scanners/manifest/README.md#8-how-this-applies-to-pikakube): this
repository has roughly 1,700 manifests and **no manifest validation in CI at all**. A validation
workflow is the case where a pinned `kubectl` in a runner earns its line — rendering Kustomize
overlays before handing them to [flux-schema](../../../scanners/manifest/flux-schema/README.md) —
and it is the one that needs no cluster credential whatsoever.

---

[← GitHub Actions](../README.md)
