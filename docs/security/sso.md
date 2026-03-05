# Centralizing Authentication Across Data and DevOps Tools with Entra ID Single Sign-On (SSO)

## Problem:
- Fragmented Authentication: Managing separate login credentials for tools like Grafana, Backstage, Airflow, Kafka UI, and Trino creates security risks, operational complexity, and poor user experience.
- User Experience Challenges: Requiring users to log in multiple times across different tools leads to frustration and confusion.
- Security Risks: Storing credentials in multiple systems increases the chances of exposure, and managing different authentication systems can lead to inconsistencies in access control.
- Lack of Centralized Control: Without SSO, it’s difficult to enforce uniform security policies and manage user access across different systems.

## Solution:
- SSO Integration with OAuth 2.0 and OIDC: Integrated SSO authentication with OAuth 2.0 and OpenID Connect (OIDC) protocols for tools like Grafana, Backstage, Airflow, Kafka UI, and Trino, providing secure, centralized access.
- Identity Provider Integration (GitHub and Entra ID): Configured GitHub and Entra ID as identity providers, enabling authentication with existing credentials and centralizing login across multiple tools.
- Automated Access Revocation: Entra ID automates access revocation when an employee leaves the company, ensuring security and preventing orphaned accounts.
- ServiceNow Integration for Access Requests: Integrated with ServiceNow to automate adding users to AD groups based on access requests, with approval workflows eliminando inserção manual em grupos de acesso.
- Improved Security and Compliance: SSO eliminates local credential storage and enhances access control, ensuring users can only access authorized resources with AD group-based access policies.

## Skills:
- Security

## Tools:
- Azure Entra ID
- Grafana
- Airflow
- Pomerium
- Backstage
- Kafka UI
- Trino
- Kubernetes
