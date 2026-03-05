# Scalable Event-Driven Architecture for Data Enrichment and Integration

## Problem:
- Tight Coupling & Latency: Direct integration between the Front-end and external APIs (Insiders/Athena) would cause slow response times and potential timeout issues for the end user.
- Data Incompleteness: The initial payload from the Front-end contains minimal data, requiring enrichment from a CDP (Customer Data Platform) via Athena before external delivery.
- Lack of Resilience: High traffic spikes or temporary downtime of the Insiders API could lead to data loss without a proper retry mechanism or message buffering.
- Security Risk: Hardcoding API keys or tokens for external partners within the application code creates significant security vulnerabilities.

## Solution:
- Serverless Asynchronous Pipeline: Implemented an event-driven flow using API Gateway and SQS to decouple the Front-end from the processing logic, ensuring sub-second response times.
- Scalable Data Enrichment: Developed a Python Lambda function that consumes SQS messages and utilizes Boto3 to query Amazon Athena, enriching the order data with CDP insights.
- Resilient Message Handling: Configured a Standard SQS Queue with a Dead Letter Queue (DLQ) and automatic retry logic to handle transient failures during Athena queries or Insiders API calls.
- Secure Credential Management: Integrated AWS Secrets Manager to store and retrieve Insiders API keys dynamically, ensuring no sensitive data is exposed in the code or logs.
- Data Normalization & Integration: Built custom logic within Lambda to transform enriched data into the specific contract format required by the Insiders API for customer segmentation.
- Comprehensive Observability: Utilized CloudWatch Logs & Metrics to monitor the entire execution flow, track error rates, and trigger alerts for DLQ message accumulation.
