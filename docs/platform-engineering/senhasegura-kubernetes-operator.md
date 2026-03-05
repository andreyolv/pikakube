# Custom Kubernetes Operator for Continuous Secret Synchronization with SenhaSegura

## Problem:
- Secure Database Credentials Management: In modern applications, managing database credentials securely is essential, especially in Kubernetes environments where seamless secret updates are required to avoid downtime.
- Credential Synchronization Challenge: The need to replicate and synchronize database credentials from Senha Segura Key Vault to Kubernetes Secrets, ensuring secure access with automatic credential rotation.
- External Secrets Operator Limitation: The DevOps Secrets Management (DSM) feature of Senha Segura was not enabled, and enabling it was neither quick nor straightforward. This limitation prompted the development of a custom operator tailored to this specific need.

## Solution
- Custom Kubernetes Operator: Developed the SenhaSegura Operator, a Python-based Kubernetes operator designed to automate the retrieval, creation, and updating of Kubernetes Secrets.
- OAuth 2.0 Authentication: The operator connects securely to Senha Segura Key Vault using OAuth 2.0, making GET requests every minute to fetch the latest database credentials.
- Automatic Secret Updates: When credentials change, the operator automatically updates the corresponding Secrets in Kubernetes, ensuring applications always have access to the latest credentials without experiencing downtime.
- Custom Resource Definition (CRD): A CRD was implemented to facilitate the easy injection and synchronization of Senha Segura credentials, using YAML files within Kubernetes, ensuring smooth and automated management of secrets across environments.

## Future Improvements:
- Operator using Golang / Kubebuilder

## Skills:
- Software Engineering
- DevOps
- Platform Engineering
- Site Reliability Engineering
- Security

## Tools:
- Python
- Docker
- Kubernetes
- Kubernetes Operator Pythonic Framework (Kopf)
