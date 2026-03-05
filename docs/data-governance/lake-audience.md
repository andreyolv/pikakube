# DataLake Access Auditing and Governance

## Problem:
- Untracked Access: Lack of visibility into who accesses what data in the DataLake, leading to potential security gaps and compliance risks.
- Compliance Requirements: Regulatory frameworks (e.g., GDPR, HIPAA) require detailed auditing of data access, which is difficult without centralized tracking.
- Unauthorized Access: Without monitoring, improper or malicious access to sensitive datasets can go undetected.
- Operational Inefficiency: Investigating access incidents or generating compliance reports is time-consuming and error-prone when logs are scattered or incomplete.

## Solution:
- Untracked Access: Lack of visibility into who accesses what data in the DataLake, leading to potential security gaps and compliance risks.
- Compliance Requirements: Regulatory frameworks (e.g., GDPR, HIPAA) require detailed auditing of data access, which is difficult without centralized tracking.
- Unauthorized Access: Without monitoring, improper or malicious access to sensitive datasets can go undetected.
- Operational Inefficiency: Investigating access incidents or generating compliance reports is time-consuming and error-prone when logs are scattered or incomplete.

## Skills:
- 

## Tools:
- 

locais e frequencia de acessos | semelhante existe databricks

audiencia de synapse e lake

monitoramento / auditoria de acessos pessoais ao lake e SPN | forma fácil de saber quais permissões uma pessoa ou spns tem

gestao decente de SPNs, com aplicação que usa, cada permissão tem cada SPN, quais grupos etc etc
az role assignment list --assignee xxxx --include-groups
az role assignment list --assignee xxxx --all -o table

talvems nao retonr ACLs pra lake, como fazer isso?