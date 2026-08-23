# Automated Dependency and Supply Chain Updates with Renovate

## Problem:
- Outdated and Vulnerable Dependencies: Application libraries, base images, Helm charts and Terraform providers age continuously, and updating them competes with delivery work for attention. Known vulnerabilities remain in lockfiles and manifests not because they are unknown, but because the manual upgrade work is never prioritized.

- Mutable References Across the Supply Chain: GitHub Actions referenced by tag, container images referenced by floating tag, and charts referenced by version range all resolve to something different over time. Pinning them to immutable digests is the correct fix, but pinning without an updater simply freezes the platform on versions that grow years old and unsupported.

- Fragmented Ecosystems: A platform repository is not a single package manifest. Python dependencies, Dockerfiles, Kubernetes manifests, Flux HelmReleases, Terraform modules, GitHub Actions and pre-commit hooks each have their own versioning mechanism, and native tooling covers only part of them — leaving the GitOps layer, where the cluster's actual versions live, unmanaged.

- Update Fatigue: An automated updater that opens one pull request per dependency, immediately and without grouping, produces more noise than teams can review. The predictable outcome is that the notifications are ignored, and an ignored updater provides no security benefit at all.

## Solution:
- Multi-Ecosystem Dependency Automation: Adopted Renovate to detect and update dependencies across the whole platform surface — Python packages, container images and digests, Helm charts, Flux `HelmRelease` and `OCIRepository` versions, Terraform providers and modules, GitHub Actions and pre-commit hooks — through a single tool and a single policy, covering the GitOps resources that other updaters do not read.

- Digest Pinning of GitHub Actions: Enabled the `helpers:pinGitHubActionDigests` preset to convert mutable action tags into immutable commit digests and keep them current. This resolves the most common finding reported by workflow security scanning at its source, and removes the trade-off between pinning for safety and staying up to date.

- Noise Control as Configuration: Used grouping, scheduling, concurrency limits and minimum release age to make the update stream reviewable — related updates grouped into a single pull request, majors separated from minors and patches, and a stability delay so freshly published releases are not adopted the day they appear.

- Security Updates Bypass the Schedule: Configured vulnerability-driven updates to ignore the schedule, the stability delay and the concurrency limit, so a fix for a known CVE is proposed immediately while routine upgrades continue to arrive in a predictable batch.

- Selective Automerge: Enabled automerge for low-risk update classes — patch and digest updates that pass the pipeline — so the changes nobody needs to discuss do not consume review capacity, while minor and major updates remain a human decision gated by required status checks.

- Centralized Configuration Presets: Defined the organizational update policy in a shared configuration extended by each repository, so schedule, grouping rules and automerge behaviour are changed in one place and inherited everywhere, rather than drifting across per-repository configuration files.

- Visibility of the Update Backlog: Enabled the dependency dashboard so pending, rate-limited and deliberately deferred updates are visible in one issue per repository — turning the set of things not yet upgraded into an explicit, reviewable list instead of an unknown.

## Skills:
- Security
- DevSecOps
- DevOps

## Tools:
- Renovate
- Github
- Github Actions
- Docker
- Terraform
- Flux
