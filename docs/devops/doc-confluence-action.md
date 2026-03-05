# Automated Documentation Updates from Github to Confluence with Github Actions
## Problem:
- Manual Documentation Synchronization: Documentation, especially MkDocs-generated sites, often needs manual updates between GitHub repositories and Confluence, resulting in outdated or inconsistent information across platforms.
- Slow Knowledge Sharing: Lack of automation leads to delays in reflecting the latest documentation changes in Confluence, reducing collaboration efficiency.
- Human Error Risk: Manual updates may cause missing changes, formatting issues, or inconsistent content.

## Solution:
- Automated GitHub Actions Workflow: Created a GitHub Actions workflow triggered by changes in documentation files (commits/pull requests) on the main or docs branches.
- MkDocs Integration: Leveraged MkDocs to generate consistent, static documentation from Markdown files, ensuring reliable output with each update.
- Markdown to Confluence Conversion: Used tools like pandoc or custom scripts to convert MkDocs Markdown into Confluence-compatible formats (HTML or rich text).
- Confluence API Authentication: Integrated secure authentication methods (Personal Access Tokens or OAuth2) to update Confluence pages without manual intervention.
- Automated Updates: The workflow automatically: Identifies updated MkDocs files; Builds and converts the documentation; Uploads it to Confluence, ensuring proper organization and page hierarchy.
- Error Handling and Alerts: Implemented error handling to detect upload failures and notify stakeholders via Slack or email for further action.
- Role-Based Access Control (RBAC): Used Azure Entra ID for RBAC to restrict workflow triggers to authorized users only.
- Audit Logging: Maintained a log of all updates, including commit author, timestamp, and changes, for traceability and auditing.
- Continuous Improvement: Regularly improved the workflow for better handling of edge cases, Markdown conversions, and theme compatibility.

## Skills:
- 

## Tools:
- 

