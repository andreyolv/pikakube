[← Docker](../README.md)

# dockle

<https://github.com/goodwithtech/dockle>
<https://github.com/goodwithtech/dockle-action>

---

## The problem it solves

**A linter for the built image, not for the Dockerfile.** It inspects the image manifest, the
config and the layers, and reports how the image is *configured* — which is a different question
from how it was written.

The distinction matters because an image can be perfectly clean at the source level and still be
wrong:

| What dockle finds | Why the Dockerfile does not show it |
|---|---|
| The image runs as **root** | the base image set `USER root` and nothing overrode it |
| Credentials left in layers | added and deleted in a later layer — deletion does not remove the earlier layer |
| Credentials in environment variables | inherited from a base image |
| World-writable files and directories | created by a package installation, not by any explicit instruction |
| `setuid` / `setgid` binaries | present in the base image |
| No `HEALTHCHECK`, no `CMD`, unused `ENV` | assembled across several stages |
| **CIS Docker Benchmark** items | the benchmark is about the image, not the source |

The credentials point is the one worth internalising. A secret `COPY`ed in and `rm`ed in a later
instruction is still in the layer where it was added, and anyone who can pull the image can
extract it. dockle looks at the layers, so it sees it; a Dockerfile reviewer sees a deletion and
moves on.

It runs against an image in a registry or a local tarball, needs no daemon, and produces
checkpoint-style output that maps to CIS benchmark items — which makes it easy to attach to a
compliance requirement.

## When to use it

- **in CI, after the build and before the push** — the natural gate, because it inspects exactly
  the artefact that would be published
- as a check against images from third parties, where there is no Dockerfile to read at all
- where a CIS Docker Benchmark statement is required and something has to produce evidence
- alongside [hadolint](../hadolint/README.md), which checks the other half

## When not to use it

- **as a vulnerability scanner** — it does not have a CVE database and does not read package
  versions. Scanning is Trivy, Grype, Clair and friends under
  `infrastructure/security/3-container/`
- as a replacement for admission control: it reports, and it does not stop anything from running
- as the only check on a Dockerfile — many problems are cheaper to catch at the source, which is
  [hadolint](../hadolint/README.md)
- on images built by [Buildpacks](../../buildpacks/README.md) expecting the same signal; those
  images are constructed by a platform that already handles most of what dockle checks

## Notes

Recorded links:

- <https://github.com/goodwithtech/dockle> — the tool.
- <https://github.com/goodwithtech/dockle-action> — the GitHub Actions wrapper, which is how it
  gets into a pipeline without an installation step.

Both were recorded together, which is the useful signal about intent: this is meant to run in CI
on every build, not to be invoked by hand when someone remembers.

The pairing with [hadolint](../hadolint/README.md) in the same folder is deliberate and worth
stating as a rule:

| Stage | Tool | Input |
|---|---|---|
| Before the build | **hadolint** | the Dockerfile |
| After the build, before the push | **dockle** | the image |
| Before deployment | a vulnerability scanner | the image's package inventory |

Skipping the middle step is the common gap, and it is the one that lets an image that runs as root
with a token baked into a layer reach a registry.

## Where it fits here

Documented as a reference rather than deployed — nothing in this repository runs it yet. The
place it belongs is the build pipeline, between the build and the push, next to
[hadolint](../hadolint/README.md).

---

[← Docker](../README.md)
