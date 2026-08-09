[← Cloud policies](../README.md)

# Cloud Custodian

<https://github.com/cloud-custodian/cloud-custodian>

<https://cloudcustodian.io>

---

## The problem it solves

Every scanner in `../../scan/` can tell you that an EBS volume is unencrypted, that an
instance has been idle for three weeks, or that a resource has no owner tag. None of them
does anything about it. Cloud Custodian is the tool that **acts**.

A policy is YAML with three parts — a resource type, a set of filters, and a set of
actions:

```yaml
policies:
  - name: stop-untagged-instances
    resource: aws.ec2
    filters:
      - "tag:owner": absent
    actions:
      - type: mark-for-op
        tag: custodian_cleanup
        op: stop
        days: 4
      - type: notify
        # ...
```

That example shows the pattern worth learning first: it does not stop anything today. It
tags the resource, schedules the action for four days out and notifies someone. A later run
picks up the tag and executes. This is `mark-for-op`, and it is the difference between
automation people trust and automation people disable.

The other thing that separates Custodian from the scanners is **how it runs**. The same
policy file executes in several modes:

| Mode | How it triggers | Use |
|---|---|---|
| `pull` | CLI or cron, queries the API | the default; audits and scheduled sweeps |
| `cloudtrail` | a CloudTrail event | react the moment a resource is created misconfigured |
| `periodic` | a scheduled Lambda in the account | serverless, no runner to operate |
| `config-rule` | AWS Config evaluation | integrates with the account's compliance view |

Event mode is what makes it a **guardrail** rather than a report: a bucket created with
public access can be corrected within seconds of the API call that created it, before
anything is written to it.

Coverage is AWS first, with Azure and GCP supported to a lesser depth. The project is part
of the CNCF.

## When to use it

| Situation | Why Custodian |
|---|---|
| The same findings come back every scan and nobody fixes them | automate the fix instead of re-reporting it |
| Tag hygiene must be enforced (ownership, cost centre, environment) | this is its single most common production use |
| Cost cleanup: idle instances, unattached volumes, orphaned snapshots, old AMIs | FinOps is arguably its biggest real-world footprint |
| Misconfigurations must be corrected at creation time | `cloudtrail` mode |
| Many accounts need the same policy set | `c7n-org` runs a policy suite across an organisation |
| Notification is the desired action, not enforcement | `c7n-mailer` delivers to email, Slack or a queue |

## When not to use it

| Situation | Use instead |
|---|---|
| The requirement is an assessment against a benchmark | `../../scan/README.md` — Prowler maps to CIS and compliance frameworks; Custodian does not |
| The resource does not exist yet | `../../iac/README.md` — cheaper to block in the pull request than to remediate after apply |
| Kubernetes objects are the target | Kyverno or Gatekeeper (`security/2-cluster/policies/`) — Custodian has a Kubernetes provider, but it is not where the ecosystem is |
| Preventive control is achievable | an SCP, an Azure Policy `deny` or a GCP org policy stops the action outright; remediating after the fact always leaves a window |
| Nobody can own the policy repository | unmaintained automation with delete permissions is worse than no automation |

## Notes

The original note recorded one link:

- <https://github.com/cloud-custodian/cloud-custodian> — the project.

The reason it sits in `policies/` rather than in `scan/` is the whole argument of the parent
folder, so it is worth stating in full here: **detection and remediation are different
capabilities with different risk profiles.** A scanner that is wrong produces a false
positive and wastes someone's afternoon. A remediation policy that is wrong takes an action
against production infrastructure, at machine speed, across every account it is pointed at.

Both halves of that are true simultaneously and neither should be softened:

- Automated remediation is the only thing that ever closes the loop. Findings lists grow
  without bound; a policy that fixes the class of problem does not.
- Automated remediation is the most dangerous thing in this entire folder. `terminate` on a
  filter that matches more than intended is not recoverable, and the run finishes before
  anyone notices.

The guardrails that make it safe are not optional extras:

```bash
# never run a new policy any other way the first time
custodian run --dryrun -s ./out policy.yml

# see exactly which resources matched, as JSON
custodian report -s ./out policy.yml
```

- **`--dryrun` first, always**, and read the matched resource list rather than the count.
- **Start with `notify` and `tag`**, not with `stop`, `delete` or `terminate`.
- **Use `mark-for-op`** so there is a grace period and a visible tag on the resource before
  anything happens to it.
- **Set resource limits** — Custodian supports capping a policy at a maximum number or
  percentage of matched resources, which turns a catastrophic run into a failed run.
- **Scope by account and region explicitly.** A policy written for a sandbox that gets run
  with production credentials is the standard incident.
- **Keep policies in git with review.** They are code with delete permissions; treat them
  that way.
- **Give the runner only the permissions its actions need.** A policy suite that only tags
  and notifies does not need `ec2:TerminateInstances`, and the IAM role is the last backstop
  when a filter is wrong.

---

[← Cloud policies](../README.md)
