[← Cloud posture scanning](../README.md)

# ScoutSuite

<https://github.com/nccgroup/ScoutSuite>

---

## The problem it solves

ScoutSuite is NCC Group's multi-cloud auditing tool. It collects configuration from a cloud
account using read-only API calls and renders the result as a **self-contained static HTML
report** that opens in a browser with no server, no database and no upload.

That output format is the point. Where Prowler produces a list of findings for a pipeline,
ScoutSuite produces a navigable picture of an account: services down the side, resources
inside them, findings attached to the specific resource that triggered them. For a one-off
assessment — a new account inherited from someone else, a due-diligence exercise, an
external audit deliverable — that is a materially better artifact than a CSV.

Providers covered: AWS, Azure, GCP, Alibaba Cloud and Oracle Cloud.

```bash
# runs read-only, writes a report directory you open locally
scout aws --report-dir ./scout-report
scout azure --cli
```

## When to use it

| Situation | Why ScoutSuite |
|---|---|
| A one-off assessment of an unfamiliar account | the report is explorable, which is what you need when you do not yet know the account |
| A deliverable someone non-technical will open | a single HTML tree, no tooling required to read it |
| The environment is air-gapped or data must not leave | everything runs locally and the report stays on disk |
| Alibaba or Oracle Cloud are in scope | coverage the other two tools in this folder do not have |

## When not to use it

| Situation | Use instead |
|---|---|
| A recurring, automated assessment | Prowler — maintained, and built for machine-readable output |
| Compliance framework evidence | Prowler's framework mappings are far more complete |
| The check set must reflect current cloud services | see the maintenance note below |
| Findings need to reach a SIEM | Prowler's OCSF/JSON output |

## Notes

Links and observations carried over from the original note:

- <https://github.com/nccgroup/ScoutSuite> — the project, from **NCC Group**, a security
  consultancy. That provenance explains the design: it is built for the way consultants
  work, arriving at an account they have never seen, with read-only access and a deadline
  for a report.
- <https://github.com/nccgroup/ScoutSuite/tree/master/ScoutSuite/providers/azure/rules/findings>
  — the rules directory for Azure findings. Each rule is a small JSON file with a
  description, a severity and a path-based condition over the collected configuration. This
  is the place to look to understand what a finding actually means, and it is also how you
  add or tune rules: they are data files, not code, so a custom check is a new JSON file
  rather than a plugin.
- **"Project with no update for more than a year"** — the recorded observation, and it is
  the deciding factor for tool choice here.

Say that plainly: **ScoutSuite is effectively in maintenance.** For a security scanner, that
is not cosmetic. Cloud providers ship new services and change defaults continuously; a rule
set that stops moving produces a report that looks complete and silently omits everything
introduced since the last update. The failure mode is a clean report on an account that has
real problems in services the tool does not know exist.

The reasonable position: use ScoutSuite when the **artifact** is what you need — an
explorable snapshot of an account, produced once, read by a human who knows to treat it as a
starting point. Do not build a continuous posture programme on it. That is Prowler's job,
and the gap between them is only going to widen.

---

[← Cloud posture scanning](../README.md)
