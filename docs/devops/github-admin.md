# GitHub Administration and Security Governance

## Problem:
- Inconsistent Repository Management: Lack of standardized processes for creating and managing repositories across the organization, leading to potential security risks and governance issues.
- Insufficient Access Control: Users can change repository visibility, fork repositories, or delete repositories without centralized approval.
- Lack of Authentication Enforcement: Not all members are required to use two-factor authentication (2FA), increasing the risk of unauthorized access.
- Inefficient Team Management: The absence of automated mapping between Azure Entra ID groups and GitHub teams complicates permission management.
- Unverified Domain Risks: Lack of verified domains increases the likelihood of phishing attacks and identity misuse.

## Solution:
- Automated Repository Creation: Implemented repository creation through Templates and Automation Workflows, enforcing consistent naming conventions and configurations. Manual repository creation is disabled to ensure compliance with organizational standards.
- Enabling Two-Factor Authentication (2FA): Enforced 2FA for all organization members to enhance authentication security and reduce unauthorized access risks.
- GitHub Apps and OAuth Apps Management: Regularly reviewed and managed authorized applications to ensure they adhere to organizational security policies and best practices.
- Restricting Repository Visibility and Forking: Disabled the ability for members to change repository visibility or fork repositories, ensuring sensitive code remains within the organization’s boundaries.
- Centralized Team Management: Established a standardized process for Creating Teams linked to Azure Entra ID Groups by Department, enabling efficient access management and role assignment.
- Restricting Repository Deletion and Transfers: Prevented members from deleting or transferring repositories without explicit administrative approval, preserving repository integrity.
- Restricted Team Creation: Disabled member capability to create new teams, ensuring team structures remain aligned with organizational governance policies.
- Domain Verification: Verified domains associated with the organization to prevent phishing attacks and protect the integrity of official repositories.

## Skills:
- DevOps

## Tools:
- Github
