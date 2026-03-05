# AWS Credential Governance and Standardization

## Problem:
- Inconsistent Authentication Methods: Applications, scripts, and automation tools used different AWS authentication approaches, leading to confusion, misconfigurations, and security risks.
- Credential Sprawl: AWS Access Keys and Secret Keys were created and distributed in an ad-hoc manner, often shared across teams or hardcoded in applications and CI/CD pipelines.
- Poor Credential Governance: Lack of standards for naming, rotation, scope, and ownership made it difficult to audit who had access to which AWS resources.
- Security Risks: Long-lived credentials without rotation increased the risk of leaks, unauthorized access, and compliance violations.
- Environment Drift: Different authentication patterns across development, staging, and production environments caused operational inconsistencies.
- Difficult Auditing and Incident Response: Tracing credential usage and revoking access quickly during incidents was complex without a standardized model.

## Solution:
- Standardized AWS Authentication Model: Defined a clear and documented authentication standard using AWS Access Keys and Secret Keys for programmatic access.
- Principle of Least Privilege: Created IAM users with tightly scoped policies, ensuring each application or automation tool had only the permissions it required.
- Centralized Credential Management: Established clear ownership, naming conventions, and lifecycle management for credentials across environments.
- Secure Distribution: Integrated credentials with secret management systems and CI/CD pipelines, eliminating hardcoded secrets in code repositories.
- Credential Rotation Policy: Implemented regular rotation procedures and documented operational runbooks to reduce the risk of long-lived credential exposure.
- Environment Isolation: Enforced separate credentials per environment (dev, staging, prod) to prevent cross-environment access and blast radius expansion.
- Audit and Monitoring: Enabled logging and monitoring of credential usage to support auditing, traceability, and faster incident response.
- Migration-Ready Architecture: Designed the model to allow future migration to IAM Roles or workload identity without disrupting applications.

# Padronização de Autenticação na AWS: Uso de Credenciais AWS de Acesso (Access Keys e Secret Key)

Gostaria de reforçar uma prática de segurança em nossa conta AWS de Dados:

## Uso de credenciais de usuário pessoais IAM (Access Key e Secret Key)
### Quando NÃO usar
- Em aplicações produtivas.
- Em aplicações de desenvolvimento contítuo, onde ambiente produtivo já está certo de existir ou já existe.

### Quando pode usar
- Pode ser usada para testes e desenvolvimentos rápidos para explorar se ferramentas e funcionalidades poderão ser úteis, onde ambiente produtivo não está certo de existir.

## Uso de usuários IAM novos com Access Key e Secret Key usados como conta de serviço
### Quando NÃO usar
- Em aplicações produtivas.
- Em aplicações de desenvolvimento contítuo, onde ambiente produtivo já está certo de existir ou já existe.

### Por que não usar
- Uma chave de usuário vazada fornece acesso ao invasor de qualquer origem enquanto a chave a credencial não expirar, geralmente semanas ou meses para ser renovada automaticamente, caso configurado renovação.
- Qualquer nova implementação que violar este padrão de segurança será identificado pelo time de Segurança e voltará para nós como Dívida Técnica a ser corrigida. Isso gerará retrabalho para a equipe se adequar às boas práticas de segurança.

### Quando pode usar
- Caso outras alternativas mais seguras e modernas não possam ser aplicadas. Justificada escolha técnica apenas em última opção.
  Exemplo: 
  - Airbyte: 
  - OpenMetaData: 

## IAM Roles com Trust Policy
### Quando usar
- Sempre que possível, deve ser sempre a primeira opção técnica.

### Por que usar
- Não armazena credenciais no código ou arquivos. Usa-se apenas o ARN da Role.
- A aplicação assume a Role e recebe credenciais temporárias que expiram automaticamente (o que minimiza drasticamente o impacto de um possível vazamento).
- A Trust Policy (Política de Confiança) define EXATAMENTE a origem que pode assumir essa Role.
  Exemplo:
  - Apenas uma instância EC2 específica.
  - Apenas uma service account de um namespace específico do EKS.
- Com isso, mesmo que um invasor descubra o ARN da Role, ele não conseguirá assumi-la se não estiver vindo de uma origem confiável e autorizada (a Trust Policy).


Qualquer dúvida sobre a implementação de Roles, podem procurar.

Contamos com a colaboração de todos para mantermos nosso ambiente seguro!