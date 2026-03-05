# Standardization of Apache Iceberg Table Format for Lakehouse

## Problem:
- Inconsistent Table Structures: Without a standardized format, tables in the lakehouse often have different schemas, partitioning, and metadata management, leading to operational complexity.
- Query Performance Issues: Non-uniform table formats reduce performance for analytics engines and complicate optimizations such as pruning and vectorized reads.
- Governance and Compliance Challenges: Lack of standardization makes it difficult to enforce data quality, security, and access policies consistently across datasets.
- Integration Complexity: Data processing tools (Spark, Trino, DuckDB) may struggle with inconsistent table definitions, requiring additional transformations or manual intervention.

## Solution:
- Inconsistent Table Structures: Without a standardized format, tables in the lakehouse often have different schemas, partitioning, and metadata management, leading to operational complexity.
- Query Performance Issues: Non-uniform table formats reduce performance for analytics engines and complicate optimizations such as pruning and vectorized reads.
- Governance and Compliance Challenges: Lack of standardization makes it difficult to enforce data quality, security, and access policies consistently across datasets.
- Integration Complexity: Data processing tools (Spark, Trino, DuckDB) may struggle with inconsistent table definitions, requiring additional transformations or manual intervention.

## Skills:
- 

## Tools:
- 

hive metastore to iceberg, test other alternatives to hms
cdc iceberg kafka connector
spark iceberg

https://iceberg.apache.org/docs/nightly/

https://medium.com/@vincent_daniel/automating-apache-iceberg-maintenance-with-spark-and-python-ee1a253de86c
https://github.com/ThibauldC/iceberg-maintenance-examples/blob/main/python/src/maintenance.py
