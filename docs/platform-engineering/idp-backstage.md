# Service Catalog and Internal Developer Portal for Kubernetes with Backstage

## Problem:
- Fragmented Developer Experience: Teams often rely on multiple internal tools, dashboards, and repositories, making it hard to find information and slowing down development.
- Lack of Centralized Service Catalog: No unified place to view available services, their owners, APIs, and documentation, leading to duplicated work and onboarding friction.
- Inconsistent Documentation: Technical documentation is scattered across repositories, wikis, and Confluence pages, making it difficult to maintain accuracy and completeness.
- Complex Onboarding: New developers struggle to understand services, dependencies, and operational processes due to the lack of a single source of truth.
- Operational Inefficiency: Without centralization, teams spend significant time navigating different systems to perform everyday tasks like deploying services, checking CI/CD pipelines, or accessing secrets.

## Solution:
- Backstage Service Catalog: Deployed Backstage as a developer portal to centralize all internal services, APIs, documentation, and pipelines in a single UI.
- Unified Developer Experience: Provided teams with an intuitive interface to browse services, discover owners, read documentation, and access operational tools quickly.
- Plugin-Based Extensibility: Integrated custom and third-party plugins to surface CI/CD status, Kubernetes deployments, monitoring dashboards, and secrets, providing a single pane of glass for operational tasks.
- Declarative Service Metadata: Standardized service metadata (owners, environments, dependencies) stored in Git repositories, ensuring consistency and versioning.
- Improved Onboarding: Accelerated new developer onboarding by giving a comprehensive overview of services, architecture, and operational tools through a single interface.
- Operational Efficiency and Governance: Reduced manual overhead by centralizing access to resources, enforcing policies, and tracking service ownership and lifecycle.


- auth github
- custom transformers to filter specific imported github teams
- custom action
- custom plugin
- tecdoc
- kubernetes log e delete pod
- catalog
- templates
- custom frontend homepage, theme and logo
- plugins acr github etc

pagina como toda stack e links de acesso
## Skills:
- 
- 

## Tools:
- 

https://backstage.io/docs/features/search/
https://backstage.io/docs/permissions/writing-a-policy/
