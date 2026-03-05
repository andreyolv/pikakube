# Ensuring Trusted Container Images with Cosign and Kyverno
## Problem:
- Image Integrity and Security: Securing containerized applications requires ensuring that only trusted and unmodified images are deployed. Without a reliable image signing and verification system, the risk of running tampered or malicious images in production increases.

## Solution:
- Cosign for Image Signing: Implemented Cosign, a tool for signing and verifying container images, to ensure that only trusted and unaltered images are deployed. This tool cryptographically signs container images, providing verification that the image deployed is the exact one intended for use.
- Automated Image Signing: Integrated Cosign into the CI/CD pipeline to sign container images before pushing them to the registry. This automated process ensures that all images are cryptographically signed, preventing deployment of unverified images.
- Kyverno for Image Verification and Enforcement: Integrated Kyverno ClusterPolicy to enforce image verification signing policies, ensuring only signed and trusted container images are deployed in Kubernetes adn reject unsigned images.
- Security and Compliance: By combining Cosign for signing and Kyverno for verification, we built a robust security framework that ensures the integrity of deployed images, improving security posture and compliance with industry regulations.

## Skills:
- Security
- DevOps

## Tools:
- Docker
- Cosign
- Kyverno
- Azure Container Registry
- Github Actions