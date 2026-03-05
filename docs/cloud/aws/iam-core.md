# AWS IAM Governance: Tag-Based Access Control (ABAC) & Security Enforcement

## Problem:

- Attribute-Based Access Control (ABAC): Implement a scalable "provisioning-by-tag" model where user permissions are dynamically granted based on matching resource tags (e.g., Team, Project).
- Automated Self-Service Security: Enable users to perform their own password resets and MFA setup without administrative intervention.
- Least Privilege Enforcement: Standardize baseline permissions for cross-functional teams while ensuring isolation between project resources.

## Solution:
- Tag-Based IAM Policies: Authored IAM policies using Condition blocks (e.g., StringEquals: "${aws:PrincipalTag/Team}": "${aws:RequestTag/Team}") to allow resource creation and management only when tags match.
- MFA Enforcement Policy: Implemented a global "Deny-all-except-MFA" policy, forcing users to authenticate with a multi-factor device before accessing any AWS service.
- Self-Service IAM Permissions: Created specific policy statements allowing users to manage their own IAM credentials, including ChangePassword and CreateVirtualMFADevice.
- Standardized Team Roles: Developed a Terraform/CloudFormation baseline that provisions IAM groups/roles with pre-defined access to common services, keyed to the user's department tag.
- Automated Credential Lifecycle: Configured IAM password policies to enforce complexity and rotation, integrated with automated auditing to track compliant vs. non-compliant users.
