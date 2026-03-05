# Real-Time SQL Server Data Ingestion with Debezium Change Data Capture

## Problem:
- Real-Time Data Replication: Traditional batch ETL pipelines often cause delays, making it hard to replicate data in near real-time for analytics or other downstream systems, which impacts business decision-making that needs low latency.

## Solution:
- Enable CDC for SQL Server: Enabled Change Data Capture (CDC) at both the database and table levels within SQL Server to capture real-time data changes.
- CDC Log-Based: Defined CDC (Change Data Capture) based on transaction logs, as delete operations are crucial for full data replication to the lakehouse. Not all tables have timestamp columns for query-based replication, and log-based CDC imposes less load on the database compared to query-based method.
- Kafka Connector with Debezium: Implemented the Debezium Kafka Connector (deployed on Kubernetes using the Strimzi operator) to enable real-time Change Data Capture (CDC), tracking and streaming data changes (insert, update, delete) from SQL Server with minimal database impact.
- Custom Kafka Connect Docker Image: A custom Docker image was created with the necessary dependencies for Debezium's integration with SQL Server.
- Kafka Streaming: Integrated Debezium with Kafka (on Kubernetes using the Strimzi operator) to stream change events to downstream systems, ensuring the Kafka topics are always up-to-date with the latest data changes.
- Schema Registry Integration: Configured automatic schema management using Schema Registry to handle table schemas and ensure data consistency during streaming.
- Grafana Monitoring: Set up a Grafana dashboard to monitor the status of CDC processes and detect any issues, ensuring smooth data streaming and addressing potential disruptions in the CDC functionality.

## Skills:
- Data Engineering
- Data Streaming
- DevOps

## Tools:
- Apache Kafka
- Kafka Connect
- Debezium
- Schema Registry
- Docker
- Kubernetes
- Kafka UI
