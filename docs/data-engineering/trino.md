# Distributed Analytics Query Engine with Trino on Kubernetes

## Problem:
- Data Querying and Analytics at Scale: As data volume grows, the need for efficient, high-performance querying across various data sources becomes essential. Traditional systems struggle to manage the scale, complexity, and flexibility required for large-scale data analytics.
- Lack of Centralized Query Engine: A centralized, fast, and flexible query engine was needed to perform real-time analytics across diverse data sources (databases, data lakes, cloud storage) efficiently.
- Scaling Query Infrastructure: Managing the infrastructure for distributed query engines across multiple data sources presented challenges in scaling and maintaining performance without compromising availability.

## Solution:
- Trino on Kubernetes: Deployed Trino on Kubernetes to leverage its distributed architecture for fast, scalable querying. This enabled a central query engine capable of handling large-scale analytics tasks while scaling dynamically with workload demands.
- Integration with Data Sources: Integrated Trino with multiple data sources, including cloud storage, relational databases, and Delta Lakes, enabling a unified query engine to access data without replication or movement.
- Hive Metastore with Custom Dependencies: Configured a Hive Metastore on Kubernetes with custom dependencies to read from Azure Storage Accounts. This setup ensures Trino can query data stored in Azure Data Lake or Blob Storage, using Hive's catalog for seamless metadata and data access management.
- Access and Permission Management: Implemented access control on catalogs and tables, managing permissions to ensure authorized access to datasets, maintaining security and compliance.
- SSO Authentication with Microsoft Entra ID: Integrated Trino with Microsoft Entra ID for SSO (Single Sign-On) authentication, providing seamless user authentication and centralized access management to Trino, ensuring consistent security policies across the organization.

## Skills:
- Data Engineering
- DevOps
- Platform Engineering

## Tools:
- Trino
- Hive
- Kubernetes
- Microsoft Entra ID