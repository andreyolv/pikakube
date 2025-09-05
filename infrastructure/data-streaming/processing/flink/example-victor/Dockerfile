FROM flink:1.17.1

ADD jars/flink-sql-connector-kafka-1.17.0.jar /opt/flink/lib/

RUN apt-get update && apt-get install python3 python3-pip -y && pip install apache-flink