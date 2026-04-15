# S3 Inventory: Data Lake Audit and Cost Allocation

## Problem:

- Untraceable Storage Growth: Difficulty in identifying which specific partitions or directories were driving sudden cost increases in the Data Lake.
- The "Small Files" Problem: Excessive accumulation of small files causing performance degradation in Spark/Athena queries and increasing metadata overhead.
- Lack of Cost Attribution: No granular visibility to perform cost "chargeback" or "showback" between different teams or projects sharing the same bucket.
- API Scalability Limits: Standard S3 LIST operations were too slow and expensive to audit buckets containing millions of objects.

## Solution:

- S3 Inventory Configuration: Automated the generation of inventory reports in Apache ORC format to provide a managed, low-cost alternative to LIST API calls.
- Granular Cost Allocation: Utilized inventory metadata to calculate the total storage size per prefix, enabling precise cost attribution and expense splitting (rateio) between different business units.
- Small Files Identification: Developed an analytical process to pinpoint prefixes with high object counts but low total size, identifying candidates for file compaction.
- Athena-Based Analytics: Integrated inventory outputs with Amazon Athena, allowing the use of SQL to monitor growth trends and storage efficiency across deeply nested directories.
- Storage Growth Auditing: Created a baseline for storage consumption, enabling the identification of "top-talker" directories that consume the most budget.
- Lifecycle Policy Optimization: Used inventory insights to validate and trigger S3 Lifecycle policies, ensuring objects are moved to cheaper storage classes (Glacier/Instant Retrieval) based on actual usage data.
