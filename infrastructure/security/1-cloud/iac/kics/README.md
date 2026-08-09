[← IaC scanning](../README.md)

# KICS

<https://github.com/Checkmarx/kics>

<https://kics.io>

---

## The problem it solves

KICS — *Keeping Infrastructure as Code Secure* — is Checkmarx's open-source scanner for
infrastructure-as-code. It answers the same question as Checkov ("is this misconfigured
before it is applied?") with two different engineering decisions behind it:

- **It is written in Go**, so it is a single static binary and fast on large trees. Python
  scanners are noticeably slower on a repository with thousands of files.
- **Its queries are written in Rego**, the Open Policy Agent language. If a team already
  writes Rego for Gatekeeper or Conftest, the policy language is not a new thing to learn —
  it is the same one, pointed at a different input.

Format coverage is wide: Terraform, CloudFormation, Kubernetes manifests, Helm, Docker and
Docker Compose, Ansible, ARM templates, Google Deployment Manager, OpenAPI, Pulumi,
Crossplane and SAM. Output is JSON, SARIF, HTML or JUnit, so it drops into CI the same way
everything else does.

## When to use it

| Situation | Why KICS |
|---|---|
| Rego is already the organisation's policy language | one language across admission control and IaC scanning |
| Scan time is a real constraint | Go binary, no interpreter start-up, parallel by default |
| Ansible or Docker Compose are part of the estate | both are first-class here, which is not universal |
| A self-contained HTML report is wanted | built in, no extra tooling |
| A vendor-neutral second opinion is useful | different rule set from Checkov, so it surfaces different findings |

```bash
# scan a path, HTML plus SARIF output
kics scan -p . --report-formats html,sarif -o ./results

# restrict to a platform and fail only on high severity
kics scan -p . --type Kubernetes --fail-on high
```

## When not to use it

| Situation | Use instead |
|---|---|
| One scanner is all the team will maintain | Checkov has broader adoption, more documentation and a larger rule set — pick it and move on |
| Custom rules must be writable by people who do not know Rego | Checkov's YAML custom policies have a far gentler slope |
| Cross-resource reasoning is needed | Checkov's graph checks are the stronger model for rules spanning multiple resources |
| The deployed account is the target | `../../scan/README.md` — this reads files, not APIs |

Running two IaC scanners is defensible only if someone owns the duplicated findings.
Otherwise it doubles the noise and halves the attention each finding gets.

## Notes

The original note in this folder recorded only the repository:

- <https://github.com/Checkmarx/kics> — the project. The relevant fact carried by that URL
  is the owner: **Checkmarx**, an application-security vendor. As with Checkov and
  Bridgecrew, the open-source scanner is real and usable on its own, but it also functions
  as the entry point to a commercial platform. Expect the roadmap to follow the product.

Worth knowing when comparing it to the alternatives in this folder: KICS and Terrascan both
use Rego, but they are not interchangeable — the query inputs and the rule libraries are
completely different, so policies do not port between them.

---

[← IaC scanning](../README.md)
