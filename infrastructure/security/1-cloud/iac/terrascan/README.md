[← IaC scanning](../README.md)

# Terrascan

<https://github.com/tenable/terrascan>

---

## The problem it solves

Terrascan scans infrastructure-as-code against policies written in **Rego (Open Policy
Agent)**. Its coverage is the usual set — Terraform, Kubernetes manifests, Helm, Kustomize,
CloudFormation, ARM, Dockerfiles — and its rules are organised by cloud provider and by
compliance family.

The feature that actually distinguishes it from the rest of this folder is that Terrascan
can run as a **Kubernetes validating admission webhook**. Instead of only failing a
pipeline, it can refuse the manifest at the API server, which closes the gap where someone
applies YAML directly without going through CI. That is why the repository ships a Helm
chart.

## When to use it

| Situation | Why Terrascan |
|---|---|
| Rego is the house policy language | rules are plain OPA, reviewable by anyone who writes Gatekeeper policies |
| The same policies should apply in CI **and** at admission | the admission webhook mode is the reason to pick it |
| Compliance-family grouping matters for reporting | rules are tagged by provider and category out of the box |

```bash
# scan Terraform in the current directory
terrascan scan -i terraform -d .

# scan Kubernetes manifests, JSON output for CI
terrascan scan -i k8s -d ./clusters -o json
```

## When not to use it

| Situation | Use instead |
|---|---|
| Admission-time enforcement is the goal | **Kyverno or Gatekeeper** (`security/2-cluster/policies/`) — both are purpose-built for this, far more widely deployed, and do not carry an IaC scanner along for the ride |
| Breadth of formats and rules is the priority | Checkov |
| Speed is the priority | KICS |
| A tool that is unambiguously active is required | see the note below before committing to it |

The admission-webhook argument is weaker than it first sounds. In a cluster that already
runs Kyverno — as pikakube does — adding a second admission controller to enforce a second
policy language is a real operational cost for overlapping coverage.

## Notes

Links recorded in the original note, and what each one means:

- <https://github.com/tenable/terrascan> — the repository. The URL itself carries the
  project's history: Terrascan was created by **Accurics**, which was acquired by
  **Tenable**. The original `accurics/terrascan` path now redirects here. Older blog posts,
  Docker image references and CI examples still point at the old organisation, which is a
  common source of confusion when setting it up.
- <https://github.com/tenable/terrascan/blob/master/deploy/helm/values.yaml> — the Helm
  chart values. This is the deployment path for the **admission webhook** mode described
  above, not for CLI scanning; running Terrascan in CI needs nothing from this file.

**Project activity is the thing to check before adopting.** Terrascan's development slowed
markedly after the Tenable acquisition, and it has not kept pace with Checkov or with
Trivy's configuration scanner in either release cadence or rule coverage. Look at the
commit and release history on the repository before betting a pipeline on it — for a
security scanner, a stale rule set is not a neutral condition. It means new resource types
and new provider defaults go unchecked while the tool still reports a green build.

---

[← IaC scanning](../README.md)
