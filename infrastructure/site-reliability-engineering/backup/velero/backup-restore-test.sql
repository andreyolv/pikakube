-- PROCESSO PARA TESTAR BACKUP E RESTORE PELO VELERO

-- 1. Subir Postgres em workloads/system-analytics/tests/postgres
-- 2. Acessar Postgres e criar tabela e inserir registros de teste
psql -U velero -d velero
\c velero
\dt

CREATE SCHEMA myschema;
SELECT schema_name FROM information_schema.schemata;
SET search_path TO myschema;

CREATE TABLE employees (
    id serial PRIMARY KEY,
    first_name varchar(50),
    last_name varchar(50),
    email varchar(100),
    hire_date date
);

INSERT INTO employees (first_name, last_name, email, hire_date)
VALUES
    ('John', 'Doe', 'john@example.com', '2023-01-01'),
    ('Jane', 'Smith', 'jane@example.com', '2023-02-15'),
    ('Michael', 'Johnson', 'michael@example.com', '2023-03-10'),
    ('Emily', 'Brown', 'emily@example.com', '2023-04-05'),
    ('William', 'Miller', 'william@example.com', '2023-05-20'),
    ('Sophia', 'Jones', 'sophia@example.com', '2023-06-18'),
    ('James', 'Davis', 'james@example.com', '2023-07-12'),
    ('Olivia', 'Wilson', 'olivia@example.com', '2023-08-08'),
    ('Liam', 'Moore', 'liam@example.com', '2023-09-25'),
    ('Ava', 'Taylor', 'ava@example.com', '2023-10-30');

SELECT * FROM myschema.employees;

-- 3. Realizar o Backup pelo Velero
-- 4. Deletar o Postgres do Kubernetes, incluindo o PVC
-- 5. Realizar o Restore pelo Velero
-- 6. Acessar o Postgres e verificar se a tabela e registros adicionados anteriormente foram restaurados.

psql -U velero -d velero
\c velero
\dt
SELECT schema_name FROM information_schema.schemata;
SELECT * FROM myschema.employees;
