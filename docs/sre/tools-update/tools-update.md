# Atualização de Ferramentas Kubernetes

## Procedimento
- Seguir atualizações na ordem de ambientes: DEV, QA(se houver) e PRD.
- Atualizar versões dos helm charts e das imagens.
- Internalizar imagem pública pra container registry privado e adequar ferramenta para usar imagem interna, caso necessário.
- Ferramentas que tenham PV/PVC, realizar backup pelo Velero antes da atualização pra garantir maior resiliência.
- Verificar na documentação e releases do GitHub se existe alguma observação importante sobre a atualização de versão.
- Atualizar apiVersion dos CustomResourceDefinitions da ferramenta, caso necessário.
- Verificar se o nome de métricas utilizadas em alertas não foram atualizadas. Atualizar alertas e dashboards no prometheus e grafana, caso necessário.
- Enviar comunicados sobre atualizações das ferramentas de criticidade alta.

## Frequência
- Executar upgrades no mínimo a cada 6 meses para todas as ferramentas.
- Executar upgrades antes no término do perídio de suporte Standard da versão do EKS para não ter custos adicionais. 
https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html
https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html

- Estabelecer calendário anual com melhores períodos para atualização, levando em consideração sazonalidades e importâncias do negócio.
- Comunicar janela de manutenção as partes interessadas.

## Procedimento EKS
https://docs.aws.amazon.com/eks/latest/userguide/platform-versions.html

- Verificar possíveis issues da versão nova em https://github.com/kubernetes/kubernetes/issues
- Atualizar versão do control plane
- Atualizar versão node group
- Atualizar versões dos Add-ons
 - Se houver erro marcar configuração de override.
- Atualizar versão da VM do Karpenter, não é atualizado sozinho, é preciso drenar os nós gerenciados pelo karpenter.

kubectl drain xxxxxxxxxxxxxxxx --ignore-daemonsets --delete-emptydir-data

kubectl get pods -A --field-selector spec.nodeName=xxxxxxxxxxxxxxxxx \
  -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name' --no-headers | \
  while read namespace name; do
    echo "Forçando delete do pod $name no namespace $namespace"
    kubectl delete pod "$name" -n "$namespace" --grace-period=0 --force
  done

## Exceções
- Quando identificado bug ou vulnerabilidade crítica que deve ser corrigida o mais breve possível

## Criticidade
## Nível: Baixa
**Critério (Exemplo):** Ferramentas de otimização ou ferramentas internas da área de dados.  
**Ação de Risco (Durante Update):** Downtime tolerado.  
**Ferramentas:**
- reloader
- descheduler (atualizar depois do EKS)
https://github.com/kubernetes-sigs/descheduler?tab=readme-ov-file#compatibility-matrix

- kubecost
- keda
- custom-scheduler (atualizar depois do EKS)
- metabase
- grafana
- actions-runner-controller/actions-runner-scale-set (atualizar em até 30 dias após nova versão)
https://docs.github.com/pt/actions/reference/runners/self-hosted-runners#runner-software-updates-on-self-hosted-runners

## Nível: Média Baixa
**Critério (Exemplo):** Observabilidade e segurança.  
**Ação de Risco (Durante Update):** Downtime aceitável se não houver perda de dados de observabilidade.
**Ferramentas:**
- prometheus
- fluentbit
- loki

- external-secrets
- velero

## Nível: Média Alta
**Critério (Exemplo):** Suporte a aplicações críticas ou infraestrutura (Rede/Dados).  
**Ação de Risco (Durante Update):** Downtime não desejável, mas deve ser contido com prioridade.  
**Ferramentas:**
- airbyte
- openmetadata

- aws-load-balancer-controller
- nginx-ingress
- external-dns

- cnpg
- karpenter
- kyverno

## Nível: Alta
**Critério (Exemplo):** Impacto direto sistêmico na disponibilidade de toda infraestrutura no Kubernetes.  
**Ação de Risco (Durante Update):** O downtime intolerável, deve ser minimizado ou zerado. Exige janela de manutenção formal, plano de rollback, e comunicação.  
**Ferramentas:**
- EKS
- flux
- airflow
 