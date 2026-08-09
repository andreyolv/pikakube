[← DefectDojo](../README.md)

# DefectDojo — Helm deployment

The Flux resources that install DefectDojo.

---

## What is here

| File | Resource | What it does |
|---|---|---|
| `helmrepository.yaml` | `HelmRepository` (`flux-system`) | registers `https://raw.githubusercontent.com/DefectDojo/django-DefectDojo/helm-charts` as a chart source |
| `helmrelease.yaml` | `HelmRelease` (`defectdojo`) | installs chart `defectdojo` version `1.6.152`, reconciled every 5 minutes |
| `../namespace.yaml` | `Namespace` | creates the `defectdojo` namespace |

The chart source is unusual and worth noticing: it is the **`helm-charts` branch of the
application repository**, served over `raw.githubusercontent.com`, rather than a GitHub Pages
chart repository or an OCI registry. It works, and it means chart availability depends on GitHub
raw content serving rather than on a chart host.

## What chart defaults mean here

No values are overridden, so this is an evaluation install. Four defaults matter before this
becomes anything more:

| Default | Why it needs revisiting |
|---|---|
| **Bundled PostgreSQL** | DefectDojo becomes the record of every accepted risk and every triage decision. That data belongs in a managed database with backups — see [`databases/`](../../../../../databases/README.md) |
| **No ingress** | reachable only by port-forward. Safe by accident; not a deployment |
| **Default admin credentials** | the chart generates or defaults an initial admin password. Where that value lives, and whether it is rotated, is the first thing to settle |
| **Celery workers and broker at defaults** | imports and deduplication run asynchronously; on a real ingest volume the worker configuration is what determines whether findings appear promptly |

## What is missing to make it useful

DefectDojo aggregates findings from other tools. As committed there are no importers, because
there are no other tools producing findings in CI — the only scanner deployed in this repository
is Trivy Operator, whose results currently reach Policy Reporter rather than here.

Making this productive means, in order:

1. Adopting tools that produce findings — the priority list in
   [`../../../README.md`](../../../README.md).
2. Importing from CI via the REST API, using **`reimport`** so state survives re-scans.
3. Configuring deduplication per parser, which is where the real work is —
   [`../../README.md`](../../README.md) section 2.

## Notes

- The chart values reference kept in the file:
  <https://github.com/DefectDojo/django-DefectDojo/blob/master/helm/defectdojo/values.yaml> — the
  authoritative list of every value, including the database, ingress, Celery and credential
  settings named above.

- This is one of only two things in [`../../../README.md`](../../../README.md) with committed
  manifests, the other being Renovate. Staging the aggregation layer before the tools that feed it
  is defensible sequencing, but it is worth being clear that until step 1 above happens, this
  deployment has nothing to aggregate.

---

[← DefectDojo](../README.md)
