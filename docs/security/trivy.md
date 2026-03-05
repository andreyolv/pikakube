# Container Vulnerability Scanning and Security Compliance with Trivy 

## Problem:
- Containers Vulnerability: Containers have become a fundamental part of modern applications, but they often come with security risks due to outdated or vulnerable software dependencies.
- Continuous Security: The fast-paced development cycles and the dynamic nature of containerized environments make it challenging to track and mitigate vulnerabilities, increasing the risk of breaches and compliance issues.

## Solution:
- Trivy Vulnerability Scanning: Implemented Trivy, an open-source vulnerability scanner for containers, to perform continuous scanning of container images and filesystems. Trivy helps identify vulnerabilities in both operating system packages and application dependencies, providing detailed reports on security flaws that could potentially impact containerized environments.
- Integration with CI/CD Pipeline: Integrated Trivy into the Github Actions CI/CD pipeline to automate vulnerability scanning during the build and deployment images. This ensures that every container image is thoroughly scanned for known vulnerabilities before being pushed to private container registry, preventing the deployment of potentially insecure images.
- Integration with GitHub Advanced Security: Integrated Trivy with GitHub Advanced Security to export vulnerability scan results as sarif (Static Analysis Results Interchange Format) files. These files are automatically uploaded to GitHub's Security tab, offering visibility of security issues directly in the repository. This integration allows developers to address vulnerabilities efficiently within the GitHub environment, and prioritize fixes based on the risk level and impact on the system.

## Skills:
- Security
- DevSecOps
- DevOps

## Tools:
- Trivy
- Docker
- Github Actions