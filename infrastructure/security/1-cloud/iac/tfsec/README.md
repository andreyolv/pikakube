[← IaC scanning](../README.md)

# tfsec

<https://github.com/aquasecurity/tfsec>

<https://github.com/aquasecurity/trivy>

---

> **Read this first: tfsec has been folded into Trivy.** Aqua Security merged tfsec's
> Terraform checks into Trivy's misconfiguration scanner (`trivy config`). tfsec itself is
> in maintenance — the repository is still there, but new checks and new development go to
> Trivy. **For anything new, run `trivy config`, not `tfsec`.**

## The problem it solves

tfsec was the fast, opinionated static scanner for **Terraform specifically**. Written in
Go, single binary, no interpreter, no configuration required to be useful — point it at a
directory and it reports the misconfigurations it finds, with the offending lines and a
short explanation of why each one matters.

Its design point was narrowness. It did one language, understood HCL properly rather than
by pattern-matching, resolved variables and module inputs, and returned results fast enough
to run on every save. That focus is exactly what made it the default Terraform scanner
before the merge.

Its checks did not disappear — they now live inside Trivy, alongside container image
scanning, filesystem scanning, SBOM generation and Kubernetes scanning, in one binary.

## When to use it

Almost never, for new work. The honest list:

| Situation | Verdict |
|---|---|
| An existing pipeline already runs tfsec and passes | fine to leave alone; plan the move to `trivy config` |
| Terraform-only repository, new setup | use `trivy config` — same checks, maintained |
| `tfsec` custom Rego checks already exist | Trivy accepts them; the migration is mostly mechanical |
| Terraform **plan** JSON needs scanning | Trivy handles it, and handles the rest of the estate too |

```bash
# the modern equivalent of `tfsec .`
trivy config .

# fail the build on high and critical only
trivy config --severity HIGH,CRITICAL --exit-code 1 .
```

## When not to use it

| Situation | Use instead |
|---|---|
| Anything that is not Terraform | tfsec never covered CloudFormation, Kubernetes or Helm — Checkov or KICS do |
| A long-lived pipeline being built today | Trivy, which is the maintained path |
| The deployed cloud account | `../../scan/README.md` |

## Notes

The original note recorded a single link:

- <https://github.com/aquasecurity/tfsec> — the repository. The important content is the
  banner on it: tfsec is joining the Trivy family, and users are directed to Trivy for
  ongoing development.

Why this matters beyond tool trivia: a lot of Terraform CI templates circulating on the
internet still install tfsec, and it still exits zero and prints results, so nothing signals
that the rule set is not moving. A scanner that silently stops learning about new resource
types is worse than no scanner, because it produces a green check that gets trusted.

Trivy already has a folder in this repository at `security/3-container/scan/trivy/`, which
is where the container-image side of it lives. The configuration scanner described here is
the same binary — one of the practical arguments for consolidating on it is that a single
tool then covers images, filesystems, manifests and Terraform.

---

[← IaC scanning](../README.md)
