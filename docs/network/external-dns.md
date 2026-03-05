# Automated DNS Records Management in Kubernetes with ExternalDNS

## Problem:
- Manual DNS Configuration: DNS records were managed manually via cloud consoles or external DNS systems, making the process slow and error-prone.
- Operational Bottlenecks: Application teams depended on infrastructure teams to create or update DNS entries, increasing lead time to expose services.
- Configuration Drift: DNS records frequently became outdated or orphaned when Kubernetes Services or Ingresses were modified or removed.
- Limited Visibility and Control: Difficulty tracking which Kubernetes workloads owned specific DNS records, impacting troubleshooting and governance.

## Solution:
- Deployed ExternalDNS: Implemented ExternalDNS to automatically manage DNS records based on Kubernetes Services and Ingress resources.
- Kubernetes-Native DNS Automation: Enabled automatic creation, update, and deletion of DNS records directly from Kubernetes resource definitions.
- Simplified Service Exposure: Allowed teams to expose applications using DNS by applying annotations, without manual DNS changes.
- Lifecycle-Aware DNS Management: Ensured DNS records were automatically cleaned up when services or ingresses were removed.
- Multi-Provider DNS Support: Integrated with cloud DNS providers (such as Route53, Azure DNS, and Google Cloud DNS) and on-prem DNS solutions.
- Declarative Configuration: Managed domain filters, TTLs, and provider credentials declaratively, aligned with Kubernetes best practices.
- Reduced Operational Risk: Eliminated human error in DNS changes and reduced the risk of stale or conflicting records.
- Faster Delivery: Reduced DNS provisioning time from hours or days to seconds, improving deployment speed and reliability.

## Skills:
- 

## Tools:
- 
