import os

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings


def main():
    # Create streaming environment
    env = StreamExecutionEnvironment.get_execution_environment()

    settings = EnvironmentSettings.new_instance()\
                      .in_streaming_mode()\
                      .use_blink_planner()\
                      .build()

    # create table environment
    tbl_env = StreamTableEnvironment.create(stream_execution_environment=env,
                                            environment_settings=settings)

    # add kafka connector dependency
    kafka_jar = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'flink-sql-connector-kafka_2.11-1.13.0.jar')

    tbl_env.get_config()\
            .get_configuration()\
            .set_string("pipeline.jars", "file://{}".format(kafka_jar))

    #######################################################################
    # Create Kafka Source Table with DDL
    #
    # - The Table API Descriptor source code is undergoing a refactor
    #   and currently has a bug associated with time (event and processing)
    #   so it is recommended to use SQL DDL to define sources / sinks
    #   that require time semantics.
    #   - http://apache-flink-mailing-list-archive.1008284.n3.nabble.com/DISCUSS-FLIP-129-Refactor-Descriptor-API-to-register-connector-in-Table-API-tt42995.html
    #   - http://apache-flink-user-mailing-list-archive.2336050.n4.nabble.com/PyFlink-Table-API-quot-A-group-window-expects-a-time-attribute-for-grouping-in-a-stream-environment--td36578.html
    #######################################################################
    src_ddl = """
        CREATE TABLE salesitems (
            seller_id VARCHAR,
            product VARCHAR,
            quantity INT,
            product_price DOUBLE,
            sale_ts BIGINT,
            proctime AS PROCTIME()
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'salesitems',
            'properties.bootstrap.servers' = 'localhost:9092',
            'properties.group.id' = 'tumbling-window-sql',
            'format' = 'json'
        )
    """

    tbl_env.execute_sql(src_ddl)

    # create and initiate loading of source Table
    tbl = tbl_env.from_path('salesitems')

    print('\nSource Schema')
    tbl.print_schema()

    #####################################################################
    # Define Tumbling Window Aggregate Calculation of Revenue per Seller
    #
    # - for every 30 second non-overlapping window
    # - calculate the revenue per seller
    #####################################################################
    sql = """
        SELECT
          seller_id,
          TUMBLE_START(proctime, INTERVAL '30' SECONDS) AS window_start,
          TUMBLE_END(proctime, INTERVAL '30' SECONDS) AS window_end,
          SUM(quantity * product_price) AS window_sales
        FROM salesitems
        GROUP BY
          TUMBLE(proctime, INTERVAL '30' SECONDS),
          seller_id
    """
    windowed_rev = tbl_env.sql_query(sql)

    print('\nProcess Sink Schema')
    windowed_rev.print_schema()

    ###############################################################
    # Create Kafka Sink Table
    ###############################################################
    sink_ddl = """
        CREATE TABLE processedsales2 (
            seller_id VARCHAR,
            window_start TIMESTAMP(3),
            window_end TIMESTAMP(3),
            window_sales DOUBLE
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'processedsales2',
            'properties.bootstrap.servers' = 'localhost:9092',
            'format' = 'json'
        )
    """
    tbl_env.execute_sql(sink_ddl)

    # write time windowed aggregations to sink table
    windowed_rev.execute_insert('processedsales2').wait()

    tbl_env.execute('sql-tumbling-windows-demo')


if __name__ == '__main__':
    main()
