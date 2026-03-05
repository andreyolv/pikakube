# Secretless Workload Authentication in Kubernetes with Workload Identity

## Problem:
- Secret-Based Authentication Risks: Applications running in Kubernetes often rely on static secrets (tokens, keys, credentials), increasing the risk of leaks and credential sprawl.
- Credential Rotation Overhead: Manually rotating secrets across multiple workloads and namespaces is operationally complex and error-prone.
- Over-Privileged Access: Shared credentials make it difficult to enforce least-privilege access at the workload level.
- Poor Auditability: Mapping cloud or infrastructure access back to specific Kubernetes workloads is difficult when using shared service accounts or static - credentials.
- Security Gaps in Multi-Cluster Environments: Managing credentials consistently across multiple clusters increases complexity and security risk.

## Solution:
- Workload Identity for Kubernetes: Implemented workload identity to allow Kubernetes workloads to authenticate using their native ServiceAccount identity, - eliminating the need for static secrets.
- Pod-Level Identity Mapping: Bound Kubernetes ServiceAccounts directly to infrastructure or platform identities, enabling fine-grained, least-privilege - access per workload.
- Short-Lived Credentials: Leveraged token exchange mechanisms to issue short-lived credentials dynamically, reducing the blast radius of compromised - identities.
- Improved Security Posture: Removed long-lived secrets from manifests, ConfigMaps, and CI/CD pipelines.
- Audit and Traceability: Enabled clear traceability between infrastructure access and the originating Kubernetes workload for auditing and compliance.
- Multi-Cluster Ready: Standardized identity patterns across clusters to ensure consistent security controls and simplified operations.
- Seamless Application Integration: Applications authenticate transparently without code changes, relying on Kubernetes-native identity mechanisms.

## Tools:

solicitação de criação de projeto por backstage
automação backstage cria managed identity ia crossplane
output do client-id do managed identity insere no label de service account default do namespace
  labels: 
    azure.workload.identity/client-id:

bug, task não tá pegando o client id do service account, ta precisando passar como variavel no pod
testar passar serviceaccount default no executor config

ver alguma forma de passar via mutation label            labels={"azure.workload.identity/use": "true"}) em todos as tasks, mutation policy talvez

AZURE_TENANT_ID e AZURE_FEDERATED_TOKEN_FILE são montados automaticamente quando usa os labels
AZURE_CLIENT_ID deveria montar automatico tbm, mas ta bugado

esperar spark 4.0 pra funcionar workload identity, pra atualizarem a versão do hadoop azure com esse pacote.