# Airflow Policies

Todas as DAGs do Airflow DEVEM seguir as políticas definidas a seguir.
Caso a DAG não cumpra alguma das políticas, não será deployada e irá aparecer um erro (AirflowClusterPolicyViolation) informando a violação da politica no cabeçalho do airflow werbserver.

https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/cluster-policies.html

## Motivação

- Evitar DAGs e Tasks travadas em execução por muito tempo no Airflow;

- Importante garantir que todas as Tasks sejam alocadas nas namespaces existentes, para que por erros de sintaxe o Airflow não tente alocar em namespaces inexistente e perda performance;

- Garantir que todas as Tasks sejam alocadas no namespace específico do projeto, para que o custo do Cluster Kubernetes seja vinculado corretamente ao projeto;

- Através da Padronização as DAGs , Melhorar performance da Ferramenta, Dar visibilidade na utilização de recursos por projeto e com isso ratear corretamente os custos do Cluster Kubernetes.

## Políticas

1. Dagrun_timeout

1.1 DAG deve ter parâmetro 'dagrun_timeout' de tipo datetime.timedelta.

1.2 Valor do parâmetro dagrun_timeout deve ser menor que 24 horas.


2. Owners

2.1 Deve existir o parâmetro 'owner' no dicionário do default_args.


3. Namespace

3.1 Deve existir o parâmetro executor_config nas tasks, exceto EmptyOperator.

3.2 Deve existir o parâmetro 'namespace' no executor_config nas tasks.

3.3 Valor do parâmetro namespace deve ser o namespace correto do projeto'.


4. Recursos

4.1 Deve existir o parâmetro ‘cpu' no executor_config nas tasks.

4.2 Deve existir o parâmetro 'memory' no executor_config nas tasks.


## Exemplos

imagens: 





## Recomendações

Uso do .airflowignore

 O Airflow verifica todos arquivos python pra verificar se o arquivo é uma DAG ou não, com uso do .airflowignore podemos ignorar todos os arquivos de tasks. Isso vai ajudar a remover erros de imports de tasks no cabeçalho do airflow e diminuir a carga do dag processor.

 O .airflowignore funciona exatamente igual ao .gitignore e deve estar no mesmo diretório das DAGs.

Exemplo:





.airflowignore vai ignorar os diretórios conf e modules que contém os arquivos python de tasks e configurações.

 Mais informações sobre .airflowignore:
https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#airflowignore
