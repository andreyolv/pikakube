# Docker Image Internalization from Public Container Registry to Private Container Registry
## Problem:
- Pull Limits on Public Container Registries: Public container registries often impose pull limits, causing issues when frequently deploying applications at scale in Kubernetes.
- Lack of Image Immutability: Without controls, Docker images can be updated with the same tag, leading to inconsistencies between deployments and making it difficult to track changes.
- Security and Compliance: External images may lack proper security scans, making them vulnerable. There is a need to enforce security policies, such as vulnerability scanning (e.g. Trivy), to ensure the integrity of infrastructure images.
- Governance and Auditability: Managing a large number of images in a container registry without a clear structure or audit trail can lead to confusion and compliance issues.

## Solution:
- Internalization of Images: A process was implemented to automate the transfer of Docker images from public registries to a private container registry, using GitHub repository and GitHub Actions workflow. This ensures images remain within the organization’s infrastructure, improving control over the deployment lifecycle.
- Governance and Security: Images are scanned using Trivy to identify vulnerabilities before being used in the Kubernetes cluster. This enhances security and ensures compliance with internal standards.
- Container Registry Organization with Prefixing: A naming convention was introduced for images stored in the private registry adding a prefix to each image to indicate its source registry facilitates better organization and management of internalized images.
- Auditability and Change Tracking: GitHub Actions workflows ensure that all changes to images are tracked and auditable, providing visibility into when images were internalized, tagged, and scanned for vulnerabilities.

## Skills:
- DevOps
- Security

## Tools:
- Docker
- Kubernetes
- Github Actions
- Trivy
- Azure Container Registry

avaliar harbor para algo genérico pq aws meio merda
