https://github.com/dbt-labs/dbt-core
https://github.com/dbt-labs/jaffle-shop-classic
https://github.com/elementary-data/elementary
https://github.com/dbt-labs/metricflow


https://github.com/duckdb/dbt-duckdb
https://github.com/getindata/dbt-flink-adapter

TO DO
- Integrar com Cosmos no Airflow.
- Integrar com DuckDB.
- Integrar com Flink.

python3 -m venv venv
source venv/bin/activate
deactivate

pip install dbt-core # python3 -m pip install --upgrade dbt-core

# Trusted Adapters https://docs.getdbt.com/docs/trusted-adapters
pip install dbt-spark
pip install dbt-postgres
pip install dbt-trino

# Community Adapters https://docs.getdbt.com/docs/community-adapters
pip install dbt-clickhouse
pip install dbt-duckdb
pip install dbt-starrocks
pip install dbt-risingwave
pip install dbt-flink-adapter

dbt --version

dbt init exemplo pra criar primeira vez, depois não precisa

or
deploy kubernetes postgres ou no docker: sudo docker run --name owspostgres -e POSTGRES_PASSWORD=1234 -p 5432:5432 -d postgres
k port-forward svc/postgres 5432

conectar banco no dbeaver

criar schema 'transactional' no dbeaver
CREATE SCHEMA transactional;

pip install sqlalchemy
pip install psycopg2-binary

Importar os csvs como tabelas no postgres.
python3 import_tables.py

Check 
SELECT * FROM transactional.city;

export PASS=postgres123

dbt run

comando 'dbt seeds' se os csvs estiverem dentro da pasta seed tbm carrega os os csvs como tabelas, porem 
não é recomendado, pois é limitado, ajustes em dados precisa ser feito no arquivo, e via python pode ser feito 
usando o pandas pra tratar antes de carregar

dbt docs generate
dbt docs serve

dbt run

dbt test

--- DBT FLINK
https://github.com/getindata/dbt-flink-adapter
https://medium.com/@aminesnoussi7/introducing-the-dbt-flink-adapter-execute-real-time-analytics-on-apache-flink-with-dbt-run-a892bbdacbfb
https://risingwave.com/blog/streaming-dbt-the-right-way-to-unlock-stream-processing-with-risingwave/
https://getindata.com/blog/dbt-run-real-time-analytics-on-apache-flink-announcing-the-dbt-flink-adapter/
https://github.com/gliter/dbt-flink-adapter-example

https://www.getdbt.com/assets/uploads/dbt_certificate_study_guide.pdf
