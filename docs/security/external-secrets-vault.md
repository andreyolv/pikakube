# Kubernetes Secret Synchronization between Azure Key Vault and External Secrets Operator

## Problem:
- Manual Secret Rotation: Although Sealed Secrets is a popular tool for encrypting secrets in Kubernetes, it requires the manual creation and rotations of SealedSecrets. Manual updates to secrets can result in operational overhead and increase the risk of using outdated or compromised credentials.
- Compliance and Security Concerns: Organizations must adhere to strict security and compliance standards, ensuring that secrets are managed properly, rotated regularly, and kept secure. Storing secrets in a non-centralized or poorly protected manner can lead to compliance violations and security vulnerabilities.

## Solution:
- Centralized Secret Management with Azure Key Vault: Stores and manages sensitive information such as secrets, keys, and certificates. It helps organizations enhance security by providing centralized access control, encryption, and audit logging, ensuring compliance and protecting critical data.
- External Secrets Operator for Kubernetes Integration: Leveraged the External Secrets Operator to connect Azure Key Vault with Kubernetes clusters. This tool dynamically synchronizes secrets from Azure Key Vault into Kubernetes workloads, enabling seamless and automated secret injection without exposing sensitive information.
- Dynamic Secret Rotation: With Azure Key Vault’s built-in rotation capabilities, secrets are automatically kept up-to-date and synchronized with Kubernetes. This eliminates manual updates and minimizes the risk of human error while ensuring that secrets are always fresh and secure.

## Skills:
- Site Reliability Engineering
- Security
- Cloud Computing
- DevOps

## Tools:
- Hashicorp Vault / Azure Key Vault
- External Secrets Operator
- Kubernetes
