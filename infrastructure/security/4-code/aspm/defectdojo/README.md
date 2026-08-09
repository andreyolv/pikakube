[← ASPM](../README.md)

# DefectDojo

<https://github.com/DefectDojo/django-DefectDojo>

Deployment: [`helm/`](helm/README.md)

---

## The problem it solves

DefectDojo is the open-source vulnerability management platform: the place every scanner's output
lands, gets deduplicated, and acquires an owner and a state.

Its decisive feature is the **parser library** — 180+ importers covering essentially every tool
in this tree and most commercial ones. Trivy, Grype, Semgrep, CodeQL, bandit, gosec, gitleaks,
TruffleHog, ZAP, Nuclei, osv-scanner, Dependency-Check, Nessus, Burp, and generic SARIF. That
breadth is why it is the default answer to aggregation: whatever you adopt next, a parser
probably exists.

The model it imposes:

| Concept | What it is |
|---|---|
| **Product Type / Product** | the application or service a finding belongs to — this is the ownership axis |
| **Engagement** | a testing activity, either a one-off assessment or a continuous CI-driven stream |
| **Test** | one tool's run within an engagement |
| **Finding** | a single issue, with severity, state, description and remediation |
| **Endpoint** | where it was found, for the DAST side |

Around that it provides deduplication (configurable per parser, with several hash strategies),
**risk acceptance with an expiry date**, false-positive tracking, SLA configuration per severity,
metrics and trends, JIRA integration, and a full REST API — which is how findings get imported
from CI rather than uploaded by hand.

Two capabilities worth singling out:

- **`reimport` rather than `import`.** Re-importing a scan into the same test *updates* existing
  findings, closes ones that no longer appear, and reopens ones that came back — preserving state
  across runs. Using `import` instead creates a new set every time and destroys the history,
  which is the most common way people make DefectDojo useless to themselves.
- **Risk acceptance with an expiry.** The state model directly supports the discipline argued for
  throughout this tree: an acceptance is temporary and dated, not permanent and invisible.

It is a Django application, and it is a real deployment: web application, database, Celery workers
and a broker.

## When to use it

- **Several tools producing findings in different formats**, and nobody able to answer "what is
  outstanding" without opening five dashboards
- **You need findings to have state** — reviewed, accepted until a date, false positive — that
  survives re-scanning
- **Trends and metrics** for people who will never open a scanner: findings over time, mean time
  to remediate, which services are accumulating
- **Mixed environments** — CI findings, cluster findings, DAST results, and a penetration test
  report, in one place. This is where it clearly beats GitHub code scanning
- **You want open source and self-hosted**, which distinguishes it from most of the commercial
  ASPM market

## When not to use it

- **One or two tools.** It is a substantial deployment; two dashboards do not justify it — see
  [`../README.md`](../README.md) section 5
- **Everything already emits SARIF into GitHub code scanning.** That is aggregation, free and
  already running. Move when it stops being enough
- **No one will triage.** A platform without a process is a better-organised way of ignoring
  findings
- **You will not tune deduplication.** Out of the box it will either duplicate or over-merge for
  your tool mix, and the tuning is the actual work
- **You want it to find things.** It finds nothing; it organises what others found
- **You cannot operate a Django application with a database.** Backups, upgrades and the database
  are yours. Chart defaults are for evaluation, not for a system that becomes the record of every
  security decision

## Notes

Original note recorded for this tool:

- <https://github.com/DefectDojo/django-DefectDojo> — the upstream project (OWASP). The repository
  holds the application, the **Helm chart** (which is what the release here installs, served
  straight from the `helm-charts` branch), the parser list and the documentation for the data
  model, deduplication configuration, the REST API and the CI import scripts.

From the manifests committed here:

- The chart comes from `https://raw.githubusercontent.com/DefectDojo/django-DefectDojo/helm-charts`
  — note this is a **branch of the application repository served as a chart repository**, not a
  separate charts repo or an OCI registry. Chart `defectdojo` version `1.6.152`, in the
  `defectdojo` namespace.
- The values reference kept in the file:
  <https://github.com/DefectDojo/django-DefectDojo/blob/master/helm/defectdojo/values.yaml>.
- **No values are overridden**, so this is chart defaults: bundled database, no ingress, no
  configured authentication, and the default admin credential handling. Fine for evaluation;
  not fine for a system that will hold the record of every accepted risk — see
  [`helm/README.md`](helm/README.md).

Two operational notes worth keeping visible:

- **Use `reimport`, not `import`, from CI.** This is the single most consequential detail in
  running DefectDojo well, and it is easy to get wrong on the first integration.
- **Deduplication must be configured per parser** before the data is worth trusting. The
  defaults are a starting point, not a setting.

---

[← ASPM](../README.md)
