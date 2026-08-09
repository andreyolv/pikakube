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
  Action. Runs the scan on pull requests and uploads SARIF, so findings appear as annotated
  lines in the diff instead of in a log nobody opens.
- <https://github.com/bridgecrewio/checkov/blob/main/docs/7.Scan%20Examples/Helm.md> — how
  Helm scanning works. Worth reading before relying on it: Checkov renders the chart to
  plain manifests first, so results depend on the values used at render time. Scanning a
  chart with default values does not tell you what your deployment looks like.
- <https://github.com/bridgecrewio/checkov/blob/main/docs/7.Scan%20Examples/Kubernetes.md>
  — the equivalent for raw manifests.
- <https://www.checkov.io/5.Policy%20Index/kubernetes.html> — the full index of Kubernetes
  policies with their `CKV_K8S_*` identifiers. This is the page to open when deciding which
  checks to enable, and when writing a suppression that needs a specific ID.

One piece of provenance that affects tool choice: Checkov comes from **Bridgecrew**, which
was acquired by **Palo Alto Networks** and folded into Prisma Cloud. The CLI remains open
source and actively maintained, but the roadmap belongs to a commercial CSPM product. That
is not a reason to avoid it — it is a reason not to be surprised by the upsell paths in the
documentation.

---

[← IaC scanning](../README.md)
