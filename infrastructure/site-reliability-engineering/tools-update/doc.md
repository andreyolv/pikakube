# Procedimento

- Seguir atualizações na ordem de ambientes: DEV, QA e PRD.
- Atualizar versões dos helm charts e das imagens.
- Internalizar imagem pública pra container registry privado e adequar ferramenta para usar imagem interna.
- Ferramentas que tenham PV/PVC, realizar backup pelo Velero antes da atualização pra garantir maior resiliência.
- Verificar na documentação e releases do GitHub se existe alguma observação importante sobre a atualização de versão.
- Atualizar apiVersion dos CustomResourceDefinitions da ferramenta, caso necessário.
- Atualizar alertas e dashboards no prometheus e grafana, caso necessário.
- Enviar comunicados sobre atualizações das ferramentas: AKS, Airflow.

# Criticidade
## Baixa
- cert-manager
- velero (atualizar imagem apenas quando compatívei com as versões dos plugins)
- keda
- marquez
- opencost
- replicator
- reloader
- elasticsearch/kibana (instalar novo operator e reapontar fluentd/fluentbit)
- grafana
 
## Média
- prometheus
- sealed-secrets
- nginx-ingress-controller
- pomerium (deixa pra lá, travado ainda esse)
- gatekeeper
- kube-scheduler | descheduler (atualizar junto do AKS)
- kubecost (atentar caso mudar api pra extração de dag de custos)
- external-secrets
- fluentd/fluentbit
- ocean-kubernetes-controller (agora já tá ok versão do helm chart, só verificar nas próximas. Já é atualizado automaticamente a minor e bugfix, verificar atualização de major eventualmente apenas. Aatualizar versão do kubernetes no Virutal Node Group após atualização de versão do Kubernetes)
- AKS (antes de atualizar rodar ferramenta pra check deprecated apiVersions)
 
## Alto
- airflow (verificar dags de checkup e manutenção após atualização.)
- kafka
- flux
