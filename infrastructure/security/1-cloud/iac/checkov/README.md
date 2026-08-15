[← IaC scanning](../README.md)

# Checkov

<https://github.com/bridgecrewio/checkov>

<https://www.checkov.io>

<https://github.com/marketplace/actions/checkov-github-action>

---

## The problem it solves

A misconfiguration written in Terraform, CloudFormation or a Kubernetes manifest is free to
fix while it is still text. Once applied it is a bucket that is already public, a volume
that is already unencrypted, a security group already open to `0.0.0.0/0` — and fixing it
becomes a change request with a blast radius instead of an edit.

Checkov reads the code before it is applied and fails the build. Its distinguishing
property is **breadth**: one binary covers Terraform, Terraform plan output,
CloudFormation, Kubernetes manifests, Helm charts, Kustomize, Serverless, ARM, Bicep,
Dockerfiles, GitHub Actions workflows and OpenAPI definitions. For a platform team that
writes several of those, one scanner and one policy language is worth more than the best
tool per format.

Two capabilities matter more than the check count:

- **Graph-based checks.** Checkov builds a graph of resources and their references, so it
  can evaluate rules that span resources — "this bucket has no logging bucket attached",
  "this security group is referenced by a public instance". Rules that only look at one
  resource block in isolation miss those entirely.
- **Custom policies in Python or YAML.** Organisation-specific rules ("every resource must
  carry a `cost-center` tag") live in the same repository as the code they check.

## When to use it

| Situation | Why Checkov |
|---|---|
| The repository holds more than one IaC format | one tool, one report, one suppression syntax |
| Kubernetes manifests and Helm charts need scanning | first-class support, not an afterthought |
| A CI gate is wanted on pull requests | the GitHub Action publishes SARIF straight into code scanning |
| Custom organisational rules are needed | YAML for simple attribute checks, Python for anything real |
| Terraform uses variables and modules heavily | scan the **plan** JSON, where every value is resolved |

Useful mechanics worth knowing before adopting it:

```bash
# scan a directory, only Kubernetes and Helm frameworks
checkov -d . --framework kubernetes helm

# scan resolved Terraform plan output rather than source
terraform plan -out tf.plan && terraform show -json tf.plan > tf.json
checkov -f tf.json

# freeze existing findings so only new ones fail the build
checkov -d . --create-baseline
checkov -d . --baseline .checkov.baseline

# machine-readable output for CI
checkov -d . -o sarif -o junitxml
```

Inline suppression carries a mandatory reason, which is the right design — it puts the
justification in the diff where a reviewer sees it:

```hcl
# checkov:skip=CKV_AWS_20:this bucket serves a public static site by design
```

## When not to use it

| Situation | Use instead |
|---|---|
| Only Terraform is in play, and speed matters | Trivy's config scanner is faster; Checkov is Python and noticeably slower on large trees |
| Enforcement is needed at the cluster admission point | an admission controller — Kyverno or Gatekeeper (`security/2-cluster/policies/`); Checkov runs in CI, not in the API server |
| The deployed account needs checking | `../../scan/README.md` — Checkov reads code, and code is not what is running |
| Container image CVEs are the concern | an image scanner (`security/3-container/scan/`); Checkov looks at configuration, not packages |
| The gate must fail on **severity** — high and above, say | not available in the open-source CLI at all: findings carry no severity, and the flags that filter by one need a Prisma Cloud key. See [the notes](#the-open-source-version-has-no-severity-levels). [KICS](../kics/README.md) and [Trivy](../../../3-container/scan/trivy/README.md) report severities without a licence |

The important limit: Checkov validates **intent**. A resource created by hand in the
console, or drifted after apply, is invisible to it. That gap is the entire reason
`../../scan/` exists as a separate capability.

## Notes

The original note in this folder read: *"Check cloud policies, images scan, helm scan,
kubernetes"* — a shorthand for the reason Checkov was recorded here in the first place: it
is not only a Terraform tool. It scans Helm and Kubernetes as well, which is what makes it
relevant to a repository whose infrastructure is mostly manifests.

Links kept from that note, and what each is for:

- <https://github.com/marketplace/actions/checkov-github-action> — the official GitHub
  Action, source at <https://github.com/bridgecrewio/checkov-action>. Runs the scan on pull
  requests and uploads SARIF, so findings appear as annotated lines in the diff instead of
  in a log nobody opens.
- <https://github.com/bridgecrewio/checkov/blob/main/docs/7.Scan%20Examples/Helm.md> — how
  Helm scanning works. Worth reading before relying on it: Checkov renders the chart to
  plain manifests first, so results depend on the values used at render time. Scanning a
  chart with default values does not tell you what your deployment looks like.
- <https://github.com/bridgecrewio/checkov/blob/main/docs/7.Scan%20Examples/Kubernetes.md>
  — the equivalent for raw manifests.
- <https://www.checkov.io/5.Policy%20Index/kubernetes.html> — the full index of Kubernetes
  policies with their `CKV_K8S_*` identifiers. This is the page to open when deciding which
  checks to enable, and when writing a suppression that needs a specific ID.

### Running it as a GitHub Action

The action is how Checkov ends up in most pipelines, and four of its inputs decide whether it is a
gate or a decoration:

| Input | Why it matters |
|---|---|
| `soft_fail` | reports findings and **exits zero**. The honest use is a first rollout on an existing repository; left on permanently, it is the *"a linter that only warns is decoration"* failure from [`code-quality/lint/`](../../../../software-engineering/code-quality/lint/README.md#1-what-a-linter-is-actually-for) |
| `baseline` | the better version of the same idea — freeze today's findings with `--create-baseline`, fail on anything **new**. This is the mechanism that makes adoption survivable |
| `framework` | scope the scan. Running every framework over a repository of Kubernetes manifests wastes minutes per job and produces findings from parsers you did not intend to run |
| `output_format` | `sarif` is what turns findings into inline annotations — and the job then needs `permissions: security-events: write` to upload it |

Two mechanical notes that cost an afternoon each if unknown. The action runs Checkov in a
**container**, so the runner's file ownership and the container's user do not always agree —
permission errors on a mounted workspace are a known wrinkle with a documented user override rather
than a bug in your workflow. And it is a **third-party action** by the rule in
[GitHub Actions §8](../../../../devops/cicd/github-actions/README.md#8-anti-patterns): pin it to a
commit SHA, and pin the Checkov version too, because new releases add checks and an unpinned scanner
fails pull requests nobody touched.

The larger point about placement is unchanged by the action: this runs **in CI, on code**. It is not
enforcement. A manifest that fails Checkov can still be applied by anyone with cluster access, which
is why the admission controllers in [`security/2-cluster/policies/`](../../../2-cluster/policies/README.md)
are a different control rather than a redundant one.

### The open-source version has no severity levels

> <https://github.com/bridgecrewio/checkov/issues/884>

The single most important limitation to know before designing a pipeline around it, and the one
that is easiest to miss because nothing announces it: **an open-source Checkov finding has no
severity.** Every check is pass or fail. There is no CRITICAL/HIGH/MEDIUM/LOW on a result, and
therefore no way to say *"fail the build on high and above, report the rest"*.

That issue — *Add Severity to controls and option to specify the severity to be reported* — asked
for exactly this, referencing Terrascan as a tool that already had it. It is **closed, and labelled
`Available in Prisma Cloud`**: severity ratings live in the platform, and the flags that filter by
them (`--soft-fail-on`, `--hard-fail-on` with severity values) need an API key against the
commercial backend. Without one, those flags only accept check IDs.

The consequences are practical rather than philosophical:

| What you wanted | What you get without a key |
|---|---|
| Fail on HIGH+, report the rest | not available — enumerate check IDs instead |
| Prioritise a first triage by severity | not available — all findings are equal |
| A severity threshold in CI, as [Kubescape's action](../../../2-cluster/posture/kubescape/README.md) offers | build your own, from ID lists |
| SARIF findings ranked in code scanning | everything arrives at one level |

The workable substitutes are the ones already described above and neither is a real replacement:
`--baseline` to freeze what exists and fail only on new findings, and explicit `--check` /
`--skip-check` lists to decide by identity what blocks a merge. Both are maintained by hand, and an
ID list is a worse instrument than a severity — it does not generalise to checks added by the next
release.

This is also the sharpest version of the provenance point below. The gap is not an oversight; it is
the product boundary, and it sits precisely where a security gate becomes useful in a large
repository. Weigh it against [Trivy's](../../../3-container/scan/trivy/README.md) config scanner and
[KICS](../kics/README.md), which report severities in their open-source form — the trade being
Checkov's breadth and graph checks against a severity field you can act on.

One piece of provenance that affects tool choice: Checkov comes from **Bridgecrew**, which
was acquired by **Palo Alto Networks** and folded into Prisma Cloud. The CLI remains open
source and actively maintained, but the roadmap belongs to a commercial CSPM product. That
is not a reason to avoid it — it is a reason not to be surprised by the upsell paths in the
documentation.

---

[← IaC scanning](../README.md)
