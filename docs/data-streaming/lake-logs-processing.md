# Spark Streaming for Temporal Data Lake Access Auditing

# Problem:

- Log Volume Overload: The sheer volume of raw access logs made it impossible to manually identify patterns or anomalies in real-time.
- Lack of Temporal Context: Individual log entries didn't show the "big picture," such as a single Service Principal performing thousands of reads in a 60-minute window (potential exfiltration).
- Delayed Analysis: Traditional batch processing of audit logs created a significant time gap between a security breach and its identification.
- Unstructured Audit Data: Raw storage logs contain excessive noise, making it difficult to isolate high-risk actions like Delete or ChangePermissions.

# Solution:

- Real-Time Stream Processing: Developed a Spark Streaming (Structured Streaming) application to ingest audit events directly from Azure Event Hubs with sub-second latency.
- Temporal Window Aggregation: Implemented Tumbling/Sliding Windows to aggregate access counts per User/Service Principal, identifying spikes in activity over specific time intervals.
- Stateful Security Auditing: Used Spark to maintain state across the stream, allowing for the detection of "Brute Force" or "Data Crawling" patterns that wouldn't be visible in single logs.
- Event Filtering & Schema Enforcement: Applied real-time transformations to filter out low-risk events and normalize the schema, focusing on high-impact actions like SetAccessControl and Delete.
- Optimized Sink Integration: Configured the processed and aggregated results to be saved into a Delta Lake table for fast forensic querying and long-term compliance reporting.
