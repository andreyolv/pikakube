# Self-Hosted GitHub Actions on Kubernetes for Secure CI/CD
## Problem:
- Accessing Internal Services via Private Endpoints: GitHub Actions workflows running on public infrastructure couldn't securely access internal services, which were only available via private endpoints. This created a significant security risk, as workflows requiring sensitive resources could not run effectively.
- Security and Compliance Issues: Running workflows on public infrastructure increased the risk of exposing sensitive tasks and violated internal security policies. Ensuring that workflows accessing critical systems remained within the secure network was a key challenge.

## Solution:
- Self-Hosted Runners with Actions Runner Controller: Deployed self-hosted GitHub Actions runners within the organization's private network using the Actions Runner Controller. This setup allowed workflows to run securely within the internal network, with access to private services through protected endpoints. The Actions Runner Controller automated runner scaling, ensuring efficient resource usage.
- GitHub Actions Runner Scale Set: Implemented a Runner Scale Set to provide scalability and high availability. The system automatically adjusted the number of runners based on workflow demands, optimizing resource usage and execution speed while ensuring the infrastructure adapted to varying workloads.
- Custom Docker Image for Dependency Management: Created a custom Docker image that included all required dependencies and tools for the workflows. This eliminated the need to install dependencies during each workflow execution, improving performance and ensuring consistency across all runs.
- Private Network for Enhanced Security: By running workflows on self-hosted runners within Kubernetes, all communications with internal services remained within the private network, mitigating security risks and adhering to compliance requirements. Sensitive data was never exposed, ensuring workflows had secure access to critical resources without compromising security policies.

## Skills:
- DevOps
- Security

## Tools:
- Docker
- Github Actions
- Kubernetes
