[← SCA](../README.md)

# osv-scanner

<https://github.com/google/osv-scanner>
<https://github.com/google/osv.dev>

---

## The problem it solves

Traditional SCA matched packages against **NVD** using CPE identifiers — a naming scheme designed
for commercial software products, not for `npm install left-pad`. Mapping an ecosystem package
onto a CPE string is guesswork, and the guesses produce both false positives (a match on a
similarly named product) and false negatives (no CPE was ever assigned).

**OSV** was built to fix exactly that. It is an open vulnerability database keyed on what package
managers actually use: ecosystem, package name, and a precise **affected version range** expressed
in that ecosystem's own version semantics. No CPE, no string matching, no guessing.

`osv-scanner` is the client:

```bash
# scan a lockfile — the recommended input
osv-scanner --lockfile=poetry.lock

# scan a whole directory tree, finding lockfiles automatically
osv-scanner -r .

# scan an SBOM or a container image
osv-scanner --sbom=sbom.spdx.json
```

What it covers: lockfiles across most major ecosystems (npm, PyPI, Go, Maven, Cargo, RubyGems,
NuGet, Composer, Hex, pub), SBOMs in SPDX and CycloneDX, container images, and Debian/Alpine
package sources.

Why the database matters more than the client: **OSV aggregates the ecosystem-native advisory
sources** — GitHub Security Advisories, PyPA, RustSec, the Go vulnerability database,
OSS-Fuzz-discovered issues, Debian and Alpine trackers — and normalises them into one schema.
Those sources are curated by the people who maintain the ecosystems, which is why the ranges are
accurate.

## When to use it

- **As the default SCA tool for a polyglot repository.** One binary, no configuration, accurate
  results, and no CPE noise
- **When false positives are the reason SCA was abandoned before.** The improvement over
  NVD/CPE-based tools is substantial and immediately visible
- **Scanning SBOMs**, which connects it to `security/0-governance/supply-chain/sbom/` — the SBOM
  becomes the input rather than a separate artefact nobody uses
- **In CI on every pull request.** It is fast enough that there is no argument about runtime
- **Alongside `govulncheck` for Go.** OSV tells you the module is affected; `govulncheck` tells
  you whether your code reaches the vulnerable function. Both use the same underlying data

## When not to use it

- **When an auditor specifically wants an OWASP Dependency-Check report.** That is a naming and
  familiarity requirement, not a technical one, and it is real —
  [`../dependency-check/README.md`](../dependency-check/README.md)
- **Expecting reachability analysis.** osv-scanner reports that a vulnerable version is present.
  Whether the vulnerable code path is reached is a separate question, addressed by `govulncheck`
  for Go and by [`../dep-scan/README.md`](../dep-scan/README.md) in part
- **Expecting it to fix anything.** It reports; [`../../dependency/README.md`](../../dependency/README.md)
  remediates
- **For deep Java analysis with shaded JARs.** A lockfile scan will not see a library repackaged
  inside another JAR; dependency-check's file-based analysis or an artefact scan will
- **If the repository has no lockfiles.** Then there is nothing precise to scan, and that is the
  problem to fix first

## Notes

Original notes recorded for this tool:

- <https://github.com/google/osv-scanner> — the scanner client, a single Go binary from Google.
  The repository documents the supported lockfile formats, the `osv-scanner.toml` configuration
  for ignoring specific vulnerability ids (with a reason and an expiry, which the format
  supports), the output formats including SARIF, and the GitHub Action.
- <https://github.com/google/osv.dev> — the database and its infrastructure. This is the more
  important of the two links conceptually: it defines the **OSV schema**, runs the aggregation of
  ecosystem advisory sources, and exposes a public API. Anything can query it, so the schema is
  now used well beyond this scanner — Trivy, Grype and Renovate all consume OSV data.

Two points worth carrying:

- **The ignore mechanism supports an expiry date** (`ignoreUntil`), which is precisely the
  discipline argued for in [`../README.md`](../README.md) — an exception that expires is a
  decision that gets revisited, and one that does not is a decision nobody makes again.
- **The database is the product.** If you already run Trivy — as this repository does — you are
  already consuming OSV data. osv-scanner is worth adding for its lockfile precision, not for a
  different set of advisories.

---

[← SCA](../README.md)
