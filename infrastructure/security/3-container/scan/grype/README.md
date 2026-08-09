[← Image scanning](../README.md)

# Grype

<https://github.com/anchore/grype>
<https://github.com/anchore/scan-action>

---

## The problem it solves

Grype is Anchore's vulnerability scanner, and its distinguishing idea is the **split between
inventory and matching**:

- **syft** produces the SBOM — it walks the image or directory and records every package it can
  identify.
- **grype** consumes an SBOM (or an image directly) and matches it against vulnerability data.

Trivy does both in one pass. Grype makes the seam explicit, and that turns out to be the reason
to choose it:

| Consequence of the split | Why it matters |
|---|---|
| Scan an SBOM instead of an image | you can re-scan a released artefact against today's database **without the image**, which is exactly what you need for something shipped to a customer or archived |
| One inventory, many scans | the expensive step (unpacking layers, identifying packages) happens once at build; re-scanning is cheap and fast |
| The SBOM is a first-class deliverable | if `0-governance/supply-chain/sbom/` is where your programme is centred, the scanner is downstream of the artefact you already produce |
| Portable evidence | the SBOM travels with the release; the scan result is reproducible from it |

Grype supports SPDX and CycloneDX as input, so the SBOM does not have to come from syft. It
sources vulnerability data from NVD, GitHub Security Advisories and the distribution trackers,
same as everything else in this folder.

`scan-action` is the GitHub Action wrapper, which uploads SARIF into GitHub code scanning.

## When to use it

- **The SBOM is the artefact and the scan is derived from it.** This is Grype's strongest case
  and the one where it beats Trivy on model rather than on features
- **You need to re-scan a release you no longer have the image for** — an archived version, a
  customer deployment, an artefact from a registry that has since been pruned
- **You already run syft.** If SBOM generation is established, adding Grype is one binary and no
  new concepts
- **You want a small, single-purpose tool.** Grype does one thing; Trivy does eight. If the
  breadth is not wanted, the narrower tool is easier to reason about
- **Comparing scanners.** Running Grype alongside Trivy on the same image is a legitimate
  one-off exercise to see how much of the difference is severity policy rather than detection

## When not to use it

- **You want one tool for images, IaC, Kubernetes and secrets.** Grype does vulnerabilities
  only; the misconfiguration and secret scanning half is not there —
  [`../trivy/README.md`](../trivy/README.md) covers it
- **You want continuous in-cluster scanning with CRDs.** There is no Grype equivalent of Trivy
  Operator in the same shape. Anchore's commercial Enterprise product addresses this; the
  open-source path does not
- **Running two scanners "for coverage."** Two scanners means two report formats, two ignore
  files and duplicated findings, with the overlap far larger than the difference. Pick one and
  aggregate if you need more —
  [`../../../4-code/aspm/defectdojo/README.md`](../../../4-code/aspm/defectdojo/README.md)
- **You will not adopt SBOM generation.** Without syft in the pipeline, Grype is just a scanner
  that does less than Trivy

## Notes

Original notes recorded for this tool:

- <https://github.com/anchore/grype> — the scanner itself. The repository documents the matching
  behaviour, the `.grype.yaml` configuration, the ignore rules (including ignoring by fix state,
  which is Grype's equivalent of `--ignore-unfixed`), and the database update mechanism.
- <https://github.com/anchore/scan-action> — the official GitHub Action. Runs Grype in a
  workflow, fails on a severity threshold, and produces SARIF for GitHub code scanning.

Not recorded in the note but part of the same story: **syft**
(<https://github.com/anchore/syft>) is the SBOM generator Grype is designed around. Reading
Grype without syft misses the point of choosing it — the pairing is the argument.

---

[← Image scanning](../README.md)
