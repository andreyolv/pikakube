import os

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, DataTypes, EnvironmentSettings
from pyflink.table.descriptors import Schema, Kafka, Json


def main():
    # Create streaming environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    settings = EnvironmentSettings.new_instance()\
                      .in_streaming_mode()\
                      .use_blink_planner()\
                      .build()

    # create table environment
    tbl_env = StreamTableEnvironment.create(stream_execution_environment=env,
                                            environment_settings=settings
                                        )
    
    # add kafka connector dependency
    kafka_jar = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'flink-sql-connector-kafka_2.11-1.13.0.jar')

    tbl_env.get_config()\
            .get_configuration()\
            .set_string("pipeline.jars", "file://{}".format(kafka_jar))


    ###############################################################
    # Create Kafka Source Table
    ###############################################################
    source_descriptor = Kafka(version="universal",
                              topic="productsales",
                              start_from_earliest=True,
                              properties={
                                'zookeeper.connect': 'localhost:2181',
                                'bootstrap.servers': 'localhost:9092',
                                'group.id': 'source-sink-demo'
                        })
    kafka_format = Json().fail_on_missing_field(True)\
                          .schema(DataTypes.ROW([
                            DataTypes.FIELD("seller_id", DataTypes.STRING()),
                            DataTypes.FIELD("product", DataTypes.STRING()),
                            DataTypes.FIELD("quantity", DataTypes.INT()),
                            DataTypes.FIELD("product_price", DataTypes.DOUBLE()),
                            DataTypes.FIELD("sales_date", DataTypes.STRING())
                          ]))
    kafka_schema = Schema().field("seller_id", DataTypes.STRING())\
                            .field("product", DataTypes.STRING())\
                            .field("quantity", DataTypes.INT())\
                            .field("product_price", DataTypes.DOUBLE())\
                            .field("sales_date", DataTypes.STRING())

    tbl_env.connect(source_descriptor)\
            .with_format(kafka_format)\
            .with_schema(kafka_schema)\
            .create_temporary_table('productsales_source')


    tbl = tbl_env.from_path('productsales_source')

    print("\nProduct Sales Kafka Source Schema")
    tbl.print_schema()


    ###############################################################
    # Create Kafka Sink Table
    ###############################################################
    sink_descriptor = Kafka(version="universal",
                            topic="productsales2",
                            properties={
                              'zookeeper.connect': 'localhost:2181',
                              'bootstrap.servers': 'localhost:9092'
                        })
    tbl_env.connect(sink_descriptor)\
            .with_format(kafka_format)\
            .with_schema(kafka_schema)\
            .create_temporary_table('productsales_sink')

    tbl.insert_into('productsales_sink')

    tbl_env.execute('source-sink-demo')


if __name__ == '__main__':
    main()

