# Software Bill of Materials (SBOM) for Supply Chain Security

## Problem:
- Lack of Dependency Visibility: Modern applications and container images include multiple transitive dependencies, making it difficult to understand what is actually running in production.
- Supply Chain Security Risks: Vulnerabilities in third-party libraries or base images can be silently introduced, increasing the attack surface.
- Slow Incident Response: Without a precise inventory of components, assessing the impact of CVEs across environments becomes time-consuming and error-prone.
- Compliance Requirements: Security and regulatory frameworks increasingly require transparency and traceability of software components.

## Solution:
- Standardized SBOM Generation: Implemented automated SBOM generation for applications and container images using industry standards such as SPDX and CycloneDX.
- CI/CD Integration: Embedded SBOM creation into build pipelines, ensuring every artifact produced has an associated and versioned bill of materials.
- Artifact Traceability: Linked SBOMs to container images and releases, enabling full traceability between deployed workloads and their dependencies.
- Security Integration: Used SBOMs as input for vulnerability scanning and CVE correlation, accelerating risk assessment and remediation.
- Governance and Auditability: Stored and versioned SBOMs to support audits, compliance checks, and post-incident analysis.

syft
cosign
policy controller | kyverno

https://github.com/actions/attest-build-provenance
https://slsa.dev/spec/v1.2-rc2/
