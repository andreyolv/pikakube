# Kafka to Delta Lakehouse: Real-Time Data Ingestion with PySpark Consumer

## Problem:
- Real-Time Data Ingestion: The need for a reliable and scalable solution to handle real-time data streams from Kafka, ensuring low-latency ingestion into Delta Lakehouse for near real-time analytics
- Kafka Consumer Requirement: Need for a Kafka consumer to read data from Kafka topics and store it in Lakehouse with Delta table format within an Azure Storage account.
- Lack of Open-Source Connector: No open-source Kafka connector available to save data in Delta table format to Azure Data Storage with SPN (Service Principal Name) authentication method.

## Solution:
- Custom Python and PySpark Consumer: Developed a Python and PySpark solution to consume data from Kafka topics and store it in the raw zone of a Lakehouse in Azure Data Storage in Delta table format, utilizing SPN authentication for secure access.
- Schema Registry Integration: Integrated the Schema Registry to read data from Kafka, using the Schema Registry key as the primary key to perform merges in the Lakehouse's raw zone.
- Modular Code Design: Created a modular codebase that can be easily reused in multiple projects, with configurable environment variables for topic names and Lakehouse paths, allowing for flexible deployments.
- Containerized Application: Containerized the application for deployment on Kubernetes, ensuring scalability and portability across environments.
- Lakehouse Delta Vaccum and Optimizate: Automated Delta Vacuum and Delta Optimizate processes using Apache Airflow, running periodically in Azure Data Storage. This approach optimizes storage size, reduces small file problems in Spark, and significantly improves Spark read performance.

## Skills:
- Data Engineering
- Data Streaming
- DevOps

## Tools:
- Apache Kafka
- Schema Registry
- Python
- Apache Spark
- Docker
- Kubernetes
