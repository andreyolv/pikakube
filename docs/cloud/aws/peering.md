# VPC Peering Cross-Account Connectivity for Data & Tech Networks

## Problem:

- Network Isolation: Data platforms and Tech microservices were running in completely isolated VPCs, preventing direct and secure communication between the two environments.
- Latency and Data Costs: Traffic between networks was forced to traverse the public internet or NAT Gateways, increasing latency and operational costs for high-volume data transfers.
- Complex Service Integration: Tools in the Tech VPC (such as APIs and applications) could not directly query or ingest data from resources in the Data VPC (Redshift, EMR, or RDS).
- Security Overhead: Relying on public endpoints or complex VPN tunnels to connect internal accounts increased the attack surface and management complexity.

## Solution:

- VPC Peering Implementation: Established a direct network connection between the Data and Tech VPCs, enabling private IP-to-IP communication across different AWS accounts.
- Route Table Optimization: Configured specific CIDR routing in both VPCs to ensure traffic is correctly directed through the peering connection, avoiding public routing.
- Cross-VPC Security Group Rules: Implemented granular Security Group rules that allow traffic only on specific ports (e.g., 5439 for Redshift, 3306 for RDS) between the peer networks.
- DNS Resolution Support: Enabled DNS hostnames resolution over the peering connection, allowing Tech services to resolve Data resources via private AWS hostnames.
