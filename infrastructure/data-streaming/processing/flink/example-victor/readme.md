# Comandos para interagir

**Preparando o ambiente**

python3 -m venv caralho

source caralho/bin/activate

deactivate

pip install confluent_kafka faker apache-flink



**Criando os tópicos**

docker exec -it kafka kafka-topics --bootstrap-server kafka:9092 --create --topic usuarios

docker exec -it kafka kafka-topics --bootstrap-server kafka:9092 --create --topic compras

bin/kafka-topics.sh --create --bootstrap-server localhost:9092 \
    --topic usuarios --partitions 1 --replication-factor 3

bin/kafka-topics.sh --list --bootstrap-server localhost:9092

**Produzindo dados no Kafka**

python produtor.py


**Acessando o flink via CLI**

docker exec -it jobmanager ./bin/sql-client.sh


**Executando queries**

SHOW TABLES;

SET sql-client.execution.result-mode = tableau;

CREATE TABLE usuarios (
    cidade      STRING,
    nome        STRING,
    bairro      STRING,
    idcompra    INTEGER
) WITH (
    'connector' = 'kafka',
    'topic' = 'usuarios',
    'properties.bootstrap.servers' = 'kafka:9092',
    'properties.group.id' = 'group.usuarios',
    'format' = 'json',
    'scan.startup.mode' = 'earliest-offset'
);


CREATE TABLE compras (
    idcompras    INTEGER,
    produto      STRING,
    preco        STRING,
    data         STRING,
    valor        INTEGER
) WITH (
    'connector' = 'kafka',
    'topic' = 'compras',
    'properties.bootstrap.servers' = 'kafka:9092',
    'properties.group.id' = 'group.compras',
    'format' = 'json',
    'scan.startup.mode' = 'earliest-offset'
);


SELECT cidade, nome, bairro, idcompra FROM usuarios;


SELECT cidade, nome FROM usuarios WHERE cidade = 'Lima';


SELECT u.cidade, u.nome, u.bairro, u.idcompra, c.produto, c.preco, c.data, c.valor
FROM usuarios u
JOIN compras c
ON u.idcompra = c.idcompras;


SELECT idcompras, produto, preco, data, valor FROM compras;


SELECT produto, preco FROM compras WHERE valor > 100;


SELECT SUM(idcompra) AS total_idcompra FROM usuarios;


SELECT SUM(idcompra) AS total_idcompra FROM usuarios WHERE bairro = 'beatae';


SELECT SUM(valor) AS total_valor FROM compras;

SELECT SUM(valor) AS total_valor FROM compras WHERE preco > '50.00';


#Usuarios que mais compram por bairro
SELECT cidade, bairro, nome, total_compras
FROM (
    SELECT cidade, bairro, nome, total_compras,
           ROW_NUMBER() OVER (PARTITION BY cidade, bairro ORDER BY total_compras DESC) as rn
    FROM (
        SELECT cidade, bairro, nome, SUM(valor) AS total_compras
        FROM usuarios u
        JOIN compras c ON u.idcompra = c.idcompras
        GROUP BY cidade, bairro, nome
    ) subquery
) ranked_data
WHERE rn = 1;