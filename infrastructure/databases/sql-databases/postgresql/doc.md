https://github.com/postgres/postgres

https://github.com/psycopg/psycopg2
https://github.com/MagicStack/asyncpg

https://github.com/citusdata/pg_cron

https://github.com/pgbackrest/pgbackrest

https://github.com/percona/pg_stat_monitor

https://github.com/le0pard/pgtune

https://github.com/CrunchyData/pg_parquet

https://github.com/pgvector/pgvector

https://github.com/citusdata/citus

https://github.com/pgaudit/pgaudit

https://www.postgresql.org/docs/current/runtime-config-resource.html

# how create user to specific database in postgres
CREATE USER my_user WITH PASSWORD 'my_password';
GRANT ALL PRIVILEGES ON DATABASE my_database TO my_user;

# how validate created users
SELECT usename FROM pg_catalog.pg_user;
SELECT datname, datacl FROM pg_database;

# pg dump
# pg_dumpall pra todos bancos lógicos, pg_dump banco especifico
kubectl exec postgres-65bcfbb67f-vrbgf -- pg_dump -U andreyolv -d teste > dbbackup.sql
k scale deploy postgres --replicas=0
k delete pvc # (não pode montar mesmos dados antigos, é equivalente a migrar pra um db novo)
atualizar imagem deployment
k scale deploy postgres --replicas=1
kubectl cp dbbackup.sql postgres-5f48985dbd-lfkcb:/tmp/dbbackup.sql
kubectl exec -it postgres-5f48985dbd-lfkcb -- psql -U andreyolv -d teste -f /tmp/dbbackup.sql

check
SELECT version();
\dt myschema.*
SELECT schema_name FROM information_schema.schemata;
SELECT * FROM myschema.employees;

https://www.postgresql.org/docs/current/logical-replication-subscription.html
