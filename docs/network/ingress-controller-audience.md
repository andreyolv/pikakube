# User Access Audience Monitoring for Pomerium Ingress Controller
## Problem:
- Access Auditing for Pomerium Ingress Controller: The need to monitor user access to applications and services managed by Pomerium. The goal was to identify underused or unused services to assess their relevance and decide whether to keep, optimize, or deprovision them to improve infrastructure efficiency and reduce costs.

## Solution:
- Pomerium Access Auditing with PostgreSQL: Implemented an access auditing solution leveraging Pomerium's built-in PostgreSQL database to log user access events. The database captures detailed information about which users are accessing which applications, at what times, and the frequency of access.
- Grafana Dashboard: Created a Grafana dashboard that queries the PostgreSQL database to visualize user access metrics in real-time. The dashboard provides insights into service usage patterns, highlighting underutilized or idle services.
- Cost Optimization: By monitoring the audience and usage of services, the project contributed to a reduction in unnecessary resource consumption, helping the organization optimize operational costs.

## Skills:
- DevOps
- FinOps
- Observability

## Tools:
- Postgres
- Pomerium
- Grafana