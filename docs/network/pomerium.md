# Granular Access for Ingress Controller via Identity Provider Groups with Pomerium

## Problem:
- Minimizing Access Security Policy: Need for a security policy that restricts access to application URLs served through the ingress controller, integrated with Entra ID identity provider. The goal is to control access to URLs based on Entra ID groups. While it's possible to achieve this with NGINX ingress controller, the presence of multiple instances of OAuth2-proxy creates inefficiencies.

## Solution:
- Pomerium Ingress Controller: Implemented Pomerium, an open-source identity-aware proxy, to streamline secure access to internal applications and services across Ingress Controller URLs. Pomerium’s integration with identity providers (IDPs) and its ability to enforce fine-grained access policies aligned with Zero Trust principles.
- Granular Access Control: Configured Pomerium to enforce strict access controls, ensuring that only authorized users can access specific Ingress Controller URLs. Simplified access management through Ingress annotations linked to Entra ID groups.

## Skills:
- DevOps
- Security

## Tools:
- Entra ID
- Pomerium
