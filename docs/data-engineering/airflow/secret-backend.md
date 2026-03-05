# Apache Airflow – Secret Backends com AWS Secrets Manager

# Motivação

Por padrão, o Airflow armazena variáveis e conexões diretamente no banco de metadados.
COm o

O uso de Secret Backends permite:

✅ Centralizar segredos em um gerenciador seguro (ex: AWS Secrets Manager).

✅ Evitar exposição de senhas no banco de metadados.

✅ Rotacionar segredos sem redeploys.

✅ Seguir práticas de segurança recomendadas (Least Privilege / IAM).

# Configuração
apache-airflow-providers-amazon

```
    env:
    - name: AIRFLOW__SECRETS__BACKEND
      value: airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend
    - name: AIRFLOW__SECRETS__BACKEND_KWARGS
      value: |-
        {
          "connections_prefix": "airflow/connections", 
          "variables_prefix": "airflow/variables", 
          "region_name": "us-east-2",
          "aws_access_key_id": "${AWS_ACCESS_KEY_ID_SECRET_BACKEND}",
          "aws_secret_access_key": "${AWS_SECRET_ACCESS_KEY_SECRET_BACKEND}"
        }
```

Como o Airflow resolve segredos

Ao requisitar uma conexão:

O Airflow busca no backend AWS Secrets Manager pelo segredo com prefixo airflow/connections/{conn_id}.

Se encontrado → retorna o valor e o utiliza diretamente.

Se não encontrado → faz fallback para o metadado local (banco Airflow).


# Referências
https://airflow.apache.org/docs/apache-airflow-providers/core-extensions/secrets-backends.html

https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/secrets-backends/aws-secrets-manager.html