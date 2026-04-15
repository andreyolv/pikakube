# Self-Hosted GitHub Actions on Kubernetes for Secure CI/CD

## Problem:
- Accessing Internal Services via Private Endpoints: GitHub Actions workflows running on public infrastructure couldn't securely access internal services, which were only available via private endpoints. This created a significant security risk, as workflows requiring sensitive resources could not run effectively.

- Security and Compliance Issues: Running workflows on public infrastructure increased the risk of exposing sensitive tasks and violated internal security policies. Ensuring that workflows accessing critical systems remained within the secure network was a key challenge.

## Solution:
- Self-Hosted Runners with Actions Runner Controller: Deployed self-hosted GitHub Actions runners within the organization's private network using the Actions Runner Controller. This setup allowed workflows to run securely within the internal network, with access to private services through protected endpoints. The Actions Runner Controller automated runner scaling, ensuring efficient resource usage.

- GitHub Actions Runner Scale Set: Implemented a Runner Scale Set to provide scalability and high availability. The system automatically adjusted the number of runners based on workflow demands, optimizing resource usage and execution speed while ensuring the infrastructure adapted to varying workloads.

- Custom Docker Image for Dependency Management: Created a custom Docker image that included all required dependencies and tools for the workflows. This eliminated the need to install dependencies during each workflow execution, improving performance and ensuring consistency across all runs.

- Private Network for Enhanced Security: By running workflows on self-hosted runners within Kubernetes, all communications with internal services remained within the private network, mitigating security risks and adhering to compliance requirements. Sensitive data was never exposed, ensuring workflows had secure access to critical resources without compromising security policies.

## Documentation Links

### Tech
- [Project](tech/project.md)
- [ADR](tech/adr.md)

### Planning
- [Business Case](planning/business-case.md)
- [RFC](planning/rfc.md)
- [Roadmap](planning/roadmap.md)
- [Tech Debt](planning/tech-debt.md)

### Ops
- [Observability](ops/observability.md)
- [Playbook](ops/playbook.md)
- [Runbook](ops/runbook.md)
- [Recovery](ops/recovery.md)
- [Upgrades](ops/upgrades.md)

### User Guide
- [Reference](user-guide/reference.md)
- [Standards](user-guide/standards.md)
- [Catalog](user-guide/catalog.md)
- [FAQ](user-guide/faq.md)

 Gemini said
GitHub Actions Self-Hosted on Kubernetes
1. Overview

This documentation details the implementation of self-hosted GitHub Actions runners within an internal Kubernetes cluster. The primary goal is to ensure that the CI/CD lifecycle occurs within the corporate network perimeter, allowing secure access to private resources and compliance with strict security policies.
2. Motivation and Challenges

Prior to this implementation, using GitHub-hosted (public) runners presented the following obstacles:

    Network Isolation: Inability to access databases, APIs, and internal services protected by Private Endpoints.

    Exposure Risks: Sensitive data traffic moving outside the private network, increasing the attack surface.

    Performance: High latency and environment setup time (dependency installation) for every workflow execution.

3. Solution Architecture
3.1 Actions Runner Controller (ARC)

We utilize the Actions Runner Controller, a Kubernetes operator that orchestrates and manages the runner lifecycle. It acts as a bridge between the GitHub API and the local cluster, dynamically registering and removing runners.
3.2 Runner Scale Sets

To address scalability challenges, we implemented Runner Scale Sets:

    Auto-scaling: The system monitors the GitHub job queue and provisions runner pods on demand.

    High Availability: Ensures that if a cluster node fails, new runners are created on healthy nodes.

    Cost Efficiency: Resources are consumed only when workflows are actively running.

3.3 Customized Docker Images

To optimize execution time (Cold Start), we developed pre-configured Docker images:

    Standardization: All necessary tools (CLIs, compilers, runtimes) are pre-installed.

    Security: Images are scanned and stored in a private registry.

    Consistency: Ensures the Build environment is identical to the Test environment.

    Custom Image Repository: The Dockerfile containing all dependencies required for standardized workflows can be found in the repository at [Link].

4. Security and Compliance Benefits
Feature	Description	Impact
Internal Traffic	All communication with private services occurs via the internal network (VPC/Subnet).	Zero exposure to the public internet.
Machine Identity	Runners can use Kubernetes Roles (RBAC) or IAM Roles (IRSA) to access cloud resources.	Eliminates the use of long-term static secrets.
Data Isolation	Logs and sensitive artifacts remain under the control of internal infrastructure.	Full compliance with LGPD (GDPR) and security standards.
5. Workflow Configuration Example

To utilize the new infrastructure, developers must point the runs-on field to the configured Scale Set name:
YAML

name: Secure Internal CI

on: [push]

jobs:
  build:
    # Name of the runner group defined in Kubernetes
    runs-on: dataops-actions-runner
        
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        
      - name: Access Private DB
        run: |
          # This command now works because the runner is inside the network
          curl http://internal-database.local/health

List of available runs-on labels:

    dataops-actions-runner: For use in the Production EKS cluster.

    dataops-actions-runner-dev: For use in the Development EKS cluster.

6. Mandatory Update Cycle

To ensure stability and secure connectivity with GitHub:

    30-Day Window: Custom images must be updated within 30 days of a new official runner release by GitHub, as per the official documentation at [Link].

    Job Blocking: Versions outdated beyond this timeframe lose compatibility with the GitHub API, resulting in failures when provisioning new jobs.
    