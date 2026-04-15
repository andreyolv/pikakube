
graph LR
    subgraph External_Sources [External Sources]
        DB[(External Databases)]
    end

    subgraph K8s_Cluster [Kubernetes Cluster]
        direction TB
        
        subgraph Ingestion_Layer [CDC Ingestion]
            Debezium[Debezium Connect]
        end

        subgraph Streaming_Platform [Event Streaming Platform]
            Kafka[Apache Kafka]
        end

        subgraph Processing_Layer [Stream Processing]
            Flink[Apache Flink]
            Spark[Spark Streaming]
        end

        subgraph OLAP_Layer [Real-time Analytics]
            StarRocks[StarRocks]
        end

        subgraph Data_Lake_Consumer [Lakehouse Sink]
            Iceberg_Consumer[Iceberg Consumer]
        end
    end

    subgraph Storage_Cloud [Cloud Storage]
        S3[AWS S3 Data Lake]
    end

    subgraph Consumption [Consumers]
        BI[BI Tools / Dashboards]
        Data_Science[Data Science / SQL Engines]
    end

    %% Data Flow
    DB -->|Change Events| Debezium
    Debezium -->|Persist Logs| Kafka
    
    Kafka -->|Stateful Processing| Flink
    Kafka -->|Micro-batch Processing| Spark
    
    Flink -->|Enriched Data| Kafka
    Spark -->|Transformed Data| Kafka
    
    Kafka -->|Real-time Ingestion| StarRocks
    Kafka -->|Sink to Iceberg Table| Iceberg_Consumer
    
    Iceberg_Consumer -->|Write Parquet/Metadata| S3
    
    %% Analytics Flow
    StarRocks --> BI
    S3 --> Data_Science
