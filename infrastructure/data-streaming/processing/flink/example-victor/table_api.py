from pyflink.table import EnvironmentSettings, TableDescriptor, TableEnvironment, Schema, DataTypes
from pyflink.table.expressions import col


env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(env_settings)

t_env.create_temporary_table(
    'kafka_source',
    TableDescriptor.for_connector('kafka')
        .schema(Schema.new_builder()
                .column('cidade', DataTypes.STRING())
                .column('nome', DataTypes.STRING())
                .column('bairro', DataTypes.STRING())
                .column('idcompra', DataTypes.STRING())
                .build())
        .option('properties.bootstrap.servers', 'kafka:9092')
        .option('properties.group.id', 'my-group')
        .option('topic', 'usuarios')
        .option('scan.startup.mode', 'earliest-offset')
        .option('value.format', 'json')
        .build())

# Criando a tabela
table = t_env.from_path("kafka_source")

# Executando um select
result_table = table.select(col("nome"), col("bairro"))

# Executando a query
result_table.execute().print()

