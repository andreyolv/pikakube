# Arquitetura do Airflow
•	Estrutural 
o	Imagem Base
o	Banco de Metadados
o	Secrets
o	Volumes de DAGs e Logs
o	Helm Chart / Kyverno


## Atualização de Airflow

how downgrade db version:
airflow db downgrade --to-version 2.7.2 (dentro de algum pod do airflow)
reverter versão da imagem no chart

## Backup EFS
https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-efs.html
