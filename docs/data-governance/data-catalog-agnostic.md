# Data Catalog GitHub Abstraction Layer

## Problem:
- Data Discovery Needs: A data catalog is essential for business users to explore and understand company data, enabling insights generation for their respective areas.
- Data Sensitivity and Risk: Storing critical data catalog information directly in an immature or unreliable tool poses risks, especially during migrations or tool replacements.
- Tool-Agnostic Centralization: There’s a need for an abstraction layer to centralize the data lake views’ metadata catalog, making it agnostic to specific tools and facilitating easier transitions between tools.

## Solution:
- Centralized Repository: Created a GitHub repository to centralize and standardize view creation in Azure Synapse Analytics and its cataloging process, streamlining management across environments.
- Catalog Enforcement: Implemented catalog creation enforcement during view deployment in production environments, ensuring comprehensive coverage of the company’s semantic data layers.
- Automated Pipeline: Developed a GitHub Actions pipeline that reads YAML files, converts them to SQL for Azure Synapse, and generates API REST requests to Azure Purview to catalog assets.
- CI/CD Pre-Check Validation: Integrated pre-check validation in the CI/CD pipeline to verify syntax before committing data to Azure Synapse and Azure Purview, preventing issues early in the process.
- Security and Permission Management: Applied the principle of least privilege by removing write access, granting read-only permissions to users, strengthening security, and ensuring proper governance.
- Delegated Approval Process: Enabled GitHub Codeowners to delegate pull request approvals to business areas, ensuring appropriate stakeholder involvement and enhancing accountability.

## Skils:
- Data Engineering
- Data Governance
- Data Catalog
- DevOps

## Tools:
- Python
- Github Actions
- Azure Synapse Analytics
- Azure Purview