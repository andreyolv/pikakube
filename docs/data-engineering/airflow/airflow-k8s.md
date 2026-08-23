# Airflow on Kubernetes
## Problem:
- deploy e manter infraestrutura de apache airflow no kubernetes de forma eficience e escalável para suportar centenas de dags rodando diarimente e milhares de tasks por dia.
- integrar repositórios de egenheiros com CICD e build

## Solution:
- Uma imabem base do airflow é construída contendo os providers e dependencias estruturais. injeção de bibliota custom.
- É recomendado pela documentação do Airflow subir um banco separado no kubernetes.
- File share pra dags e logs com CI/CD para update QA e PRD. 
- Imagens de projetos. A imagem do projeto é buildada automaticamente pelo Github Actions e a imagem armezenada no Azure Container Registry. Como buildar uma imagem ver em documentacaox.
- Multinamespace. Helm chart. Volumes de DAGs e Logs
- DAGs de Manutenção para limpeza de tabelas no banco e logs, além de dags de checkup/heartbeat para monitoramento baseline.
- Airflow policies.
- VM Spot por com possiblidade de adesão por namespace/projeto.
- Airflow SRE dahsboard no grafana e alertas .
- SSO.
- Template de Repositório, solicitação automática para criação de namespaces de projetos e repositórios via templates garantindo minha padronização.
- Key Vault
- logs via fluentbit e elastic
- sugestões de recursos airflow grafana
- kubecost e politicas de divisão de custo.
- Backup com Velero do banco (e constante operação de autalização de versão)
SLA airflow relatorio de compliance

libs operator fora de imagem base airflow
airflow sla misses

## Skills:
- Data Engineering
- DevOps
- Security
- Site Reliability Engineering

## Tools:
- Microsoft Entra ID
- Apache Airflow
- Azure Key Vault
- Helm Chart
- Velero
