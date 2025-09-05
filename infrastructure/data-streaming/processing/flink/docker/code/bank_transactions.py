import logging
import sys

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment


def python_demo():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    t_env = StreamTableEnvironment.create(stream_execution_environment=env)
    t_env.execute_sql("""
        CREATE TABLE clickstream (
            id VARCHAR,
            quantity DECIMAL(8,2),
            customer_debit VARCHAR,
            customer_credit VARCHAR,
            ts VARCHAR
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'clickstream',
            'properties.bootstrap.servers' = 'redpanda.redpanda.svc.cluster.local:9093',
            'properties.group.id' = 'test-group',
            'properties.auto.offset.reset' = 'earliest',
            'format' = 'json'
        )
    """)

    t_env.execute_sql("""
        CREATE TABLE clickstream_out
        WITH (
            'connector' = 'kafka',
            'topic' = 'clickstream_out',
            'properties.bootstrap.servers' = 'redpanda.redpanda.svc.cluster.local:9093',
            'format' = 'json'
        ) AS 
            SELECT * FROM clickstream WHERE quantity > 200
    """)

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
    python_demo()