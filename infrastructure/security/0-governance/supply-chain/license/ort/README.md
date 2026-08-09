[← License compliance](../README.md)

# ORT — OSS Review Toolkit

<https://github.com/oss-review-toolkit/ort>

---

## The problem it solves

Declared licence metadata is not good enough when the answer has to be defensible. A component
says `MIT` in its manifest and contains a vendored GPL file; another says nothing at all; a
third is dual-licensed and the metadata records only one option. Any tool reading manifests
alone reports all three as fine.

ORT is a Linux Foundation project that runs the full compliance pipeline as a chain of stages,
each of which can be run and inspected independently:

| Stage | What it does |
|---|---|
| **Analyzer** | resolves the dependency tree across many package managers, without building |
| **Downloader** | fetches the actual source of every dependency |
| **Scanner** | runs a licence **detection** engine (ScanCode, Askalono and others) over that source |
| **Advisor** | pulls vulnerability data from external sources |
| **Evaluator** | applies your policy rules to the combined result |
| **Reporter** | generates output — SPDX/CycloneDX SBOMs, **attribution documents**, NOTICE files, spreadsheets |

Two of those stages are the reason to choose it. The **Scanner** produces detected rather than
declared licences, which is the accuracy difference that matters. The **Reporter** generates
the attribution and disclosure documents that a distributed product legally needs — the
deliverable, not just the finding.

The third distinguishing feature is **curation**: ORT keeps corrections to upstream metadata as
version-controlled files, so when a package's declared licence is wrong, the fix is recorded
once and reused, rather than re-adjudicated every release.

## When to use it

- the answer must be **defensible** — due diligence, an acquisition, an audit, a product
  shipped to customers
- **attribution documents** are a deliverable: NOTICE files, disclosure documents, the
  third-party licence appendix
- upstream metadata is wrong often enough that corrections need to persist between runs —
  curation is the feature nothing else in this folder has in open source
- you want the whole thing open source and self-hosted, with no vendor and no data leaving the
  organisation
- polyglot repositories with several package managers, where per-ecosystem tools would need to
  be assembled by hand

## When not to use it

- as a fast CI gate. It downloads and scans source; runs are slow, and the failure modes are
  network- and build-shaped. [grant](../grant/README.md) is the gate, ORT is the review
- when nobody will curate. ORT's output is a starting point that assumes a human resolves
  ambiguity; unattended, the report is a large document with unresolved findings
- for a small team with no legal reviewer — the effort exceeds the exposure. See the policy
  discussion in [`../README.md`](../README.md#6-what-a-workable-policy-looks-like)
- if a managed workflow with reviewers and SLAs is what is actually wanted; that is
  [FOSSA](../fossa/README.md), and the trade is money for setup effort
- as a container image scanner — ORT works from source and package manifests, so the base
  image's OS packages are not its natural input. Combine with an SBOM-based check for those

## Notes

Original reference recorded for this tool:

> <https://github.com/oss-review-toolkit/ort>

The point worth adding is about **where ORT sits relative to everything else in this folder**.
It is the only open-source option here that does detection, curation and attribution — which
makes it the serious choice, and also the one with real setup cost. The stages are separable
for a reason: most adoptions start by running only the Analyzer to get an accurate dependency
tree, and add the Downloader and Scanner later, once someone is prepared to review what
detection turns up.

Two practical notes. **Detection produces ambiguity, not certainty** — a scanner finding three
licence texts in one package is a question for a human, and treating scanner output as an
answer rather than as evidence is the most common way ORT disappoints. And **the curation
files are the asset**: the accumulated corrections to upstream metadata are what make the
second year cheaper than the first, so they belong in version control and should survive tool
changes.

---

[← License compliance](../README.md)
