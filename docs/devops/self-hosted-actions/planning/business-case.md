# Business Case

## Problem
- GitHub-hosted runners cannot securely access internal services exposed only via private endpoints.
- Running sensitive workflows outside the private network increases security and compliance risk.

## Proposed Solution
- Run workflows on self-hosted runners inside Kubernetes within the private network using ARC and Runner Scale Sets.
- Use a custom runner image with preinstalled dependencies.

## Expected Impact
- Enable secure CI/CD for workflows that require private connectivity.
- Reduce risk of sensitive operations being executed on public infrastructure.
- Improve execution speed and consistency by removing per-job dependency installation.

## Risks
- Increased operational overhead for maintaining runner infrastructure.
- Supply chain risk: runner image must be maintained and secured.

## Success Criteria
- Workflows requiring private endpoints execute reliably.
- Compliance requirements are met for sensitive workflows.
- Runner queue time remains within acceptable limits under expected load.
