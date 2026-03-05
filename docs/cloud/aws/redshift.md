# Provisioning Amazon Redshift Serverless with Public Access Control

## Problem:

- Over-Provisioning Costs: Traditional Redshift clusters incurred fixed hourly costs regardless of actual query usage or idle time.
- Manual Cluster Management: The operational burden of patching and resizing node types slowed down the deployment of analytics environments.
- Multi-Tool Connectivity Requirements: The need to provide secure access to the data warehouse for multiple sources, including a Kubernetes cluster, a corporate VPN, and specific public-facing external tools.
- Complex Network Routing: Difficulty in balancing the need for public availability for external tools with strict security requirements.

## Solution:

- Redshift Serverless Infrastructure: Provisioned the namespace and workgroup to enable a pay-as-you-go analytics environment with no cluster management.
- Public Subnet Provisioning: Deployed the Redshift Serverless endpoints within Public Subnets to facilitate connectivity for external authorized tools.
- Layered Security Group Rules: Implemented a strict Security Group acting as a firewall, explicitly whitelisting only the VPN Static IP, the Kubernetes Cluster CIDR, and the External Tool's public IP.
- Public Accessibility Toggle: Enabled the "Publicly Accessible" setting on the Redshift Workgroup, ensuring that even with a public IP, the gateway only accepts traffic from the whitelisted sources.
- Automated Capacity Management: Configured the environment to automatically scale Base RPU based on workload, eliminating manual tuning and reducing costs during idle periods.
- Unified Infrastructure as Code: Managed the subnets, security groups, and Redshift Serverless resources within a single Terraform execution for consistent environment replication.
