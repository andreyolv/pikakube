https://github.com/dbt-labs/dbt-core
https://github.com/dbt-labs/jaffle-shop-classic
https://github.com/elementary-data/elementary
https://github.com/elementary-data/run-elementary-action

https://github.com/dbt-labs/metricflow
https://github.com/dbt-labs/dbt-adapters
https://github.com/dbt-labs/dbt-utils
https://github.com/dbt-labs/dbt-fusion

https://github.com/dbt-checkpoint/dbt-checkpoint

https://github.com/starburstdata/dbt-trino

https://github.com/dbt-labs/dbt-fusion/issues/31
https://github.com/dbt-labs/dbt-fusion/issues/38
https://github.com/dbt-labs/dbt-fusion/issues/39
https://github.com/dbt-labs/dbt-fusion/issues/829

python3 -m venv venv
source venv/bin/activate
deactivate

pip install dbt-core # python3 -m pip install --upgrade dbt-core

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
