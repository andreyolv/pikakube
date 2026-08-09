[← Image patching](../README.md)

# Copacetic

<https://github.com/project-copacetic/copacetic>

---

## The problem it solves

Copacetic (`copa`) patches vulnerable OS packages **directly into an existing container image**,
producing a new image without a rebuild and without the original Dockerfile.

The workflow is two commands:

```bash
# 1. produce a vulnerability report in a format copa understands
trivy image --vuln-type os --ignore-unfixed -f json -o report.json <image>

# 2. patch only the packages that report lists as fixable
copa patch -i <image> -r report.json -t <image>-patched
```

What happens underneath: copa uses **BuildKit** to mount the image's filesystem, runs the
distribution's own package manager to upgrade the identified packages, and writes the result as
a single new layer. The original layers are untouched, so the diff really is just the package
upgrade.

Two design decisions worth knowing:

| Decision | Consequence |
|---|---|
| **Report-driven** | copa patches what a scanner told it to patch. It is not itself a scanner, and it inherits the scanner's ignore rules — including `--ignore-unfixed`, which is what you want |
| **Patches without the report too** | recent versions can run without a report and simply upgrade all upgradable packages. Broader change, less precision. The report-driven mode is the one to prefer |

It is a **CNCF sandbox project**, originally from Microsoft.

## When to use it

- **Vendor images you cannot rebuild.** The primary case. You have neither the Dockerfile nor
  the vendor's release schedule, and the CVE is real
- **A fixed package exists but your base is pinned.** You need the package, not the base bump,
  and the base bump would drag in changes you have not tested
- **Buying time.** The rebuild is the plan; the patch is what runs until the plan lands. Provided
  it is tracked, this is a legitimate use
- **Bulk remediation across many images** — copa is scriptable and fast because it does not
  rebuild anything, which makes "patch every image in this registry" a tractable job
- **Air-gapped or slow build environments** where a full rebuild is expensive and a package
  upgrade is not

## When not to use it

- **You build the image.** Then rebuild it. Patching an image you control means creating drift
  from your own source for no reason
- **The vulnerability is in an application dependency.** copa upgrades packages known to
  `apt`/`apk`/`dnf`. A vulnerable npm package, Python wheel or JAR is invisible to it — that is
  [`../../../4-code/dependency/README.md`](../../../4-code/dependency/README.md)
- **Distroless and scratch images.** There is no package manager in the image to drive.
  Copacetic has been extending support here, but the general point stands: the smaller the base,
  the less there is to patch — and the less there was to fix in the first place
- **As a permanent strategy.** Layers accumulate, provenance decays, and eventually nobody can
  say what is in the image. Cap the number of patches before forcing a rebuild
- **Without re-signing.** The patched image is a new digest; any signature on the original no
  longer applies. If admission verification is on — see
  [`../../admission/README.md`](../../admission/README.md) — the patched image must be signed by
  you

## Notes

Original notes recorded for this tool:

- <https://github.com/project-copacetic/copacetic> — the upstream project (CNCF sandbox,
  originally Microsoft). The repository documents the `copa patch` flags, the scanner report
  formats it accepts (Trivy JSON is the main one), the BuildKit requirement, and the supported
  package managers. Also relevant there: the `copa` VEX output, which records what was patched
  in a machine-readable form.

- <https://www.youtube.com/watch?v=LBJFh1zfHjg&t=903s> — a recorded talk, linked with a
  timestamp at **15:03**, which is where the copacetic segment begins. The reason a video is
  kept as a reference for this particular tool: the value of copa is easiest to see
  demonstrated — scan, patch, re-scan, watch the finding count drop without a rebuild — and that
  demonstration is what the timestamp points at.

One practical requirement that catches people out: copa needs a **BuildKit endpoint**. Locally
that is Docker with BuildKit enabled; in CI it means either a BuildKit service or a runner where
`docker buildx` is available. It is not a single self-contained binary in the way `trivy` is.

---

[← Image patching](../README.md)
