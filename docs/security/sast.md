# Code Security with SAST and GitHub Advanced Security
## Problem:
- Lack of Proactive Vulnerability Management: The absence of an automated system to identify and address Common Vulnerabilities and Exposures (CVEs) across the organization increased the risk of security breaches and non-compliance with security standards.
- Inconsistent Security Practices: Security guidelines varied across teams, making it difficult to enforce uniform standards and track security improvements effectively.
- Limited Visibility: Without centralized monitoring, assessing the overall security posture of repositories and projects was inefficient and error-prone.

## Solution:
- dependabot, secret scaning with push protection and code scaning.
- Static Application Security Testing (SAST) Implementation: Leveraged GitHub Advanced Security with CodeQL to integrate automated static code analysis directly into the CI/CD pipeline, enabling real-time detection of CVEs and other code vulnerabilities.
- Custom Security Guidelines: Developed and enforced organization-wide security standards, including best practices for secure coding, documentation, and vulnerability remediation with examples to address common positives and false positives.
- Blocking Critical Vulnerabilities in PRs: Implemented checks to block Pull Requests (PRs) containing critical vulnerabilities, preventing insecure code from being merged into the codebase. This ensures that only secure and compliant code is promoted to production.
- Dashboard for Security Insights: Built a GitHub-based dashboard to provide a centralized view of security metrics such as percentage of secure repositories,number of CVEs detected and resolved.

## Skills:
- Security
- DevOps

## Tools:
- Github Advanced Security
- Grafana