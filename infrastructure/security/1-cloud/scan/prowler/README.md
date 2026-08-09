[← Cloud posture scanning](../README.md)

# Prowler

<https://github.com/prowler-cloud/prowler>

<https://docs.prowler.com>

---

## The problem it solves

Prowler connects to a cloud account with read-only credentials and reports what is actually
configured, checked against the **CIS Benchmark** for that provider and against a long list
of compliance frameworks mapped onto the same checks.

It is the most actively developed of the three scanners in this folder, and the only one
with genuine multi-provider parity: **AWS, Azure, GCP, Kubernetes and Microsoft 365**. The
Kubernetes provider is worth singling out — it means the same tool that assesses a cloud
account can also assess a cluster against the CIS Kubernetes Benchmark, which is unusual.

The project started life as a bash script for the AWS CIS Benchmark and was rewritten in
Python. That history explains its shape: hundreds of small, independent checks, each one
mapped to benchmark and framework identifiers, with output formats designed to be fed
somewhere rather than read in a terminal.

```bash
# full AWS assessment against CIS 2.0
prowler aws --compliance cis_2.0_aws

# a single service, one region
prowler aws --services s3 iam --region eu-west-1

# a cluster, from the current kubecontext
prowler kubernetes

# machine-readable output for a findings pipeline
prowler aws -M csv json-ocsf html
```

## When to use it

| Situation | Why Prowler |
|---|---|
| A recurring, scheduled posture assessment is needed | it is maintained, and the check set keeps up with new services |
| More than one cloud is in play | one tool, comparable output across AWS, Azure and GCP |
| A compliance framework has to be evidenced | built-in mappings to CIS, PCI DSS, HIPAA, SOC 2, ISO 27001, NIST, GDPR and others |
| Findings must feed a pipeline | OCSF/JSON output goes to a SIEM or a security data lake without a translation layer |
| The cluster should be assessed with the same tool | the Kubernetes provider covers the CIS Kubernetes Benchmark |

## When not to use it

| Situation | Use instead |
|---|---|
| Someone wants a browsable report to hand to a stakeholder, once | ScoutSuite's static HTML report is faster to produce and easier to pass around |
| The question is about code that has not been applied yet | `../../iac/README.md` — Prowler reads live APIs, so there is nothing to read before apply |
| Continuous, event-driven detection is the requirement | a managed CSPM, or AWS Config / Azure Policy — Prowler is a point-in-time scan, however often you run it |
| Remediation is expected | `../../policies/README.md` — Prowler reports, it does not act |

A practical constraint: a full multi-account scan takes real time and makes a large number
of API calls. Rate limiting and scan duration are the two things that surprise people on
first run against a large organisation.

## Notes

The original note recorded the repository and one strongly-worded opinion:

- <https://github.com/prowler-cloud/prowler> — the project.
- **"Helm chart totally amateur, low credibility"** — the recorded verdict on the project's
  Helm chart, with the evidence:
  <https://github.com/prowler-cloud/prowler/issues/7016>.

That opinion is worth keeping because it is specific and it changes a deployment decision.
The quality of the CLI and the quality of its Kubernetes packaging are separate things, and
the second is much weaker than the first. The practical consequence: **run Prowler as a
scheduled job you define yourself** — a CronJob with a read-only credential and an artifact
destination — rather than adopting the shipped chart and inheriting its assumptions. The
scanner is a batch process; there is very little a chart needs to do for it that a
twenty-line CronJob does not do more transparently.

More generally, treat the issue link as the pattern rather than the exception: for security
tooling, check whether the deployment path is as maintained as the tool itself. A
well-maintained scanner behind a neglected chart still gets deployed wrong.

One credential rule that applies to every scanner in this folder but is easiest to get
wrong here, because Prowler covers so many services: grant it a **read-only** role
(`ReadOnlyAccess` plus `SecurityAudit` on AWS, `Reader` plus `Security Reader` on Azure). A
scanner never needs write permissions, and giving it any creates exactly the
over-privileged role that `../../iam/README.md` exists to argue against.

---

[← Cloud posture scanning](../README.md)
