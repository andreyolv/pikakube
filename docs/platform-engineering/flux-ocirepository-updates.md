# Automated Version and Digest Updates for Flux OCIRepository Artifacts with Renovate

## Problem:
- Immutable References Freeze the Platform: Pinning every `OCIRepository` to an explicit tag and digest is what makes a GitOps deployment reproducible and verifiable, but without an updater the same pinning guarantees the cluster runs charts that grow months out of date, turning a supply chain control into a stagnation mechanism.

- Chart Versions Invisible to Conventional Updaters: The versions the cluster actually runs live inside Flux custom resources, not in a package manifest, so language and image updaters never see them. Renovate itself only reads `gotk-components.yaml` by default, so a repository full of Flux sources appears to have no dependencies at all.

- Manual Digest Maintenance Is Error-Prone: Bumping a tag by hand without recomputing the digest either breaks reconciliation or silently defeats the pinning, and looking up the correct digest for every artifact is exactly the kind of mechanical work that gets skipped under time pressure.

- One Pull Request per Artifact Is Unreviewable: A platform repository holding dozens of chart references produces dozens of simultaneous pull requests the moment automation is enabled. The predictable outcome is that the notifications are ignored, and an ignored updater delivers no benefit.

- Indiscriminate Scope Across Resource Kinds: A Flux repository mixes `OCIRepository`, `HelmRelease`, `HelmRepository` and `GitRepository`, each with its own versioning semantics. Updating all of them at once mixes concerns that deserve separate review and separate rollback decisions.

- Stability Delays That Suppress Updates Silently: A minimum release age is the correct guard against adopting a release the day it is published, but it depends on a release timestamp. Helm charts distributed as OCI artifacts carry no such timestamp, and the default behaviour holds every timestamp-less release as pending indefinitely — an updater that looks correctly configured, runs without errors, and proposes almost nothing.

## Solution:
- Manager Scoped to a Single Resource Kind: Enabled only the Flux manager and pointed its file patterns exclusively at manifests named `ocirepository.yaml`. Chart references remain the single update surface, while `HelmRelease`, `HelmRepository` and `GitRepository` resources stay outside the scope by construction rather than by exclusion rules that drift.

- Tag and Digest Rewritten Atomically: Relied on the Flux manager's handling of `spec.ref` fields carrying a tag, a digest, or both, so the version and its immutable digest are replaced in the same commit. Pinning and currency stop being a trade-off, and no digest is ever transcribed by hand.

- Every Suggestion Aggregated Into One Pull Request: Grouped all artifacts under a single branch and disabled the separation of major, minor and patch updates, so a week of upgrades arrives as one reviewable change set instead of one pull request per chart. Concurrency limits act as a second guard against pull request sprawl.

- Predictable Cadence With an Escape Hatch: Confined branch creation to a weekly window so the update stream lands at a known time, while the dependency dashboard keeps a checkbox to force the pull request immediately when an upgrade cannot wait for the window.

- Stability Delay That Tolerates Missing Timestamps: Kept the minimum release age but set the behaviour to treat the release timestamp as optional, so the delay still applies to registries that publish one and no longer suppresses the OCI chart registries that do not. The distinction between "no update available" and "update withheld by an internal check" is decided explicitly instead of by registry metadata.

- Verification Before Enabling: Validated the configuration and ran the updater against a local checkout in dry-run mode before granting it write access, confirming which files were matched, which artifacts were extracted, and which upgrades were withheld and why. Extraction and lookup problems are found in a local log rather than in the repository's pull request history.

- Deferred Updates Made Visible: Enabled the dependency dashboard so the full inventory of tracked artifacts, the upgrades awaiting their schedule and the references skipped as unversioned are listed in one issue, keeping what is deliberately not upgraded an explicit and reviewable set.

- Review Signal Over Changelog Volume: Disabled changelog fetching in this laboratory repository, where release notes for dozens of charts exceed the platform's pull request body limit and bury the version table that is the actual review unit. Upstream release notes remain one click away through the source link the registries expose.

- Documented Limits of the Approach: Recorded the cases automation cannot cover — references whose tag is not a version and floating tags such as `latest` are skipped by design, artifacts without a digest field receive tag-only updates, and charts whose manifests omit the source annotation offer no changelog link — so the gaps are known constraints rather than unnoticed blind spots.

## Skills:
- Platform Engineering
- GitOps
- DevOps

## Tools:
- Renovate
- Flux
- Kubernetes
- Helm
- GitHub
