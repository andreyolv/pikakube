# Cluster Homepage with Automatic Ingress URL Discovery

## Problem:
- Difficulty Discovering Services: In large Kubernetes clusters, developers and stakeholders struggle to find all deployed services and their URLs.
- Manual Documentation Overhead: Teams often maintain static lists of endpoints, which quickly become outdated and require constant updates.
- Onboarding Complexity: New team members or external users need guidance to access cluster services, slowing down onboarding and productivity.
- Lack of Centralized Entry Point: There is no single page or dashboard summarizing all exposed URLs, making navigation across services inefficient.

## Solution:
- Automated Homepage for Ingress URLs: Developed a dynamic homepage that automatically lists all services with publicly exposed URLs using Kubernetes Ingress annotations.
- Annotation-Driven Discovery: Leveraged standard annotations on Ingress resources to extract metadata like service name, owner, and description, ensuring accurate and self-updating entries.
- Centralized Cluster Entry Point: Provided a single accessible page for developers, QA, and stakeholders to navigate all cluster services without needing CLI access.
- Ease of Maintenance: Eliminated manual updates by synchronizing the homepage dynamically with cluster Ingress resources.
- Enhanced Productivity and Onboarding: New users can quickly locate relevant services and endpoints, improving workflow efficiency and reducing support requests.
- Lightweight and Extendable: Built a minimal web interface that can be extended to include additional metadata, service health, or links to dashboards.

## Skills:
- 

## Tools:
- 

