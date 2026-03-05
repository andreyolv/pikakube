# Automated Lambda Deployment via GitHub Actions

## Problem:

- Enforce Version Control Sovereignty: Establish GitHub as the "Single Source of Truth," eliminating manual, untraceable code changes directly in the AWS Console.

- Standardized Deployment Pipeline: Create a consistent, repeatable process for testing and deploying Lambda functions across multiple environments (Dev/Staging/Prod).

- Auditability and Compliance: Ensure every change to production code is linked to a specific Commit, Pull Request, and authorized Approver.

- Risk Mitigation: Prevent "Hotfixes" in the console that lead to configuration drift and make disaster recovery impossible.

- Developer Productivity: Enable developers to deploy code using familiar Git workflows, reducing the cognitive load of managing AWS infrastructure manually.

## Solution:

- CI/CD Pipeline with GitHub Actions: Engineered automated workflows that trigger on push or pull_request events to build, package, and deploy Lambda functions.

- Automated Testing Integration: Incorporated unit testing and linting steps within the pipeline to catch bugs before they reach the cloud environment.

- Secure Credential Management: Utilized GitHub Actions Secrets and OIDC (OpenID Connect) to securely authenticate with AWS without storing long-lived IAM access keys.

- Infrastructure as Code (IaC): Leveraged frameworks like SAM or Terraform to define Lambda configurations (memory, timeouts, env vars) alongside the application code.

- Deployment Strategies: Implemented "Zip" or "Container Image" deployment patterns, ensuring that the deployed artifact is identical to what was tested locally.

- Transparent Change Auditing: Enabled a clear audit trail where every AWS Lambda update is mapped back to a GitHub SHA, providing full visibility into "Who, What, and When."

- Console Access Restriction: Tightened IAM policies to prevent manual code edits in the AWS Lambda Console, enforcing the "Pipeline-Only" deployment rule.
