[← Aggregation](../README.md)

# Dependency-Track

<https://github.com/DependencyTrack/dependency-track>
<https://github.com/DependencyTrack/helm-charts>

---

## The problem it solves

A CVE is announced. Someone asks whether you are affected. Without this, the answer involves
pulling images, rescanning them, and grepping through build logs for the ones that no longer
build — a process measured in days, producing an answer nobody fully trusts.

Dependency-Track is an OWASP flagship project that stores CycloneDX SBOMs as a portfolio of
projects and continuously re-evaluates them as vulnerability data changes. The inventory is
uploaded once; the matching runs forever. When a new advisory lands, it tells you which
projects contain the affected component and at which versions, without touching a registry.

It pulls from several sources — the NVD, GitHub Advisories, OSV, Sonatype OSS Index — which
matters because coverage and identification quality differ sharply between them, particularly
for language ecosystems where NVD's CPE matching is unreliable.

Beyond vulnerability matching it carries a **policy engine**: rules over components, licences,
severities and versions, evaluated on every upload. That is what turns it from a dashboard
into something that can fail a build.

## When to use it

- the concrete question is **"which of our things contain component X?"** — this is the tool
  that answers it, and it is the question people actually ask
- SBOMs are being produced (or can be) on every build, in CycloneDX
- you want continuous monitoring rather than point-in-time scanning, and want to know about a
  disclosure without rebuilding anything
- licence policy needs enforcing from the same inventory, in the same place
- an audit requires demonstrating that dependencies are tracked over time rather than checked
  once
- as the **first** aggregation platform — it is the mature, well-understood default

## When not to use it

- SPDX is the only format available — Dependency-Track is CycloneDX-native; conversion works
  but loses fidelity, and it is friction on every upload
- the question is about **relationships** across evidence types — provenance, attestations,
  build ancestry — rather than about component inventory. That is [GUAC](../guac/README.md)
- nothing generates SBOMs yet and nobody has committed to doing so. The dashboard will be
  empty and the capability will get a reputation
- you want a scanner for a single image in CI — that is `3-container/scan/` (Trivy, Grype);
  this is the layer above it
- there is no owner for the alerts. Continuous monitoring with no recipient is a mailbox

## Notes

Original note recorded for this tool, translated:

> The documentation is rubbish.

Blunt, and worth taking seriously as a finding rather than as a complaint. The consequence in
practice: the product works, and the parts that take time are the ones documentation would
normally cover — how the API server, frontend and database components fit together in the
Helm chart, how to authenticate uploads from CI (an API key with the right permission set, not
an obvious flow), and what the project/version naming scheme should be so that findings can
later be joined to something real.

The naming scheme is the one to think about before the first upload, because it is painful to
change afterwards. `project = image name`, `version = image digest` is the shape that keeps
findings joinable to what is actually running; using a tag as the version means the record
silently describes a different artefact over time.

The chart is staged here at version `0.18.0` from `https://dependencytrack.github.io/helm-charts`,
with an empty `values:` block — so none of the above has been exercised yet. Two things will
need setting when it is: persistence for the database (the whole point is that the record
outlives the build) and enough memory for the vulnerability feed mirror, which is larger than
first-time deployers expect.

---

[← Aggregation](../README.md)
