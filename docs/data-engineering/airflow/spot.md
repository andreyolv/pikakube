# Spot

## Tipos de Máquinas Virtuais
Todas as cargas de trabalho que rodam nas instâncias de cluster kubernetes são executadas em máquinas virtuais em um cloud provider, no nosso caso a Azure.

Em relação a forma de pagamento, existem basicamente 3 classes de máquinas virtuais nos cloud providers:
•	On Demand: Paga-se conforme o uso. Recomendado para quando não existe previsibilidade do uso contínuo das máquinas.
•	Reserva de Instância: Paga-se antecipadamente pela reserva de instâncias específicas. Recomendado para quando existe previsibilidade de uso contínuo das máquinas. Fornece descontos aproximados entre 30 a 40% em relação a máquinas On Demand.
•	Spot: São sobras de máquinas sem utilização pelo cloud provider. Fornece descontos de aproximadamente 90% em relação a máquinas On Demand. E não possuem SLA, pois o cloud provider pode interromper as máquinas a qualquer momento.

## Spot Ocean
Características especificas que a solução Spot Ocean para máquinas spot oferece:
•	Monitora famílias de máquinas virtuais mais baratas e com menor probabilidade de interrupção, a fim de garantir maior disponibilidade mesmo sendo uma máquina spot, melhorando relação custo benefício. Sem a Spot Ocean, o cloud provider pode demorar alguns minutos para realocar a carga interrompida. A Ocean consegue prever quando uma máquina será desprovisionada e solicita criação de outra com antecedência.
•	Alocação heterogênea de classes de máquinas virtuais evitando desperdício de recursos. Ou seja, é possível subir uma máquina com o tamanho ideal para a carga que deseja-se alocar no momento. Ao contrário de máquinas de reserva de instâncias em que é sempre a mesma classe de máquina com mesmo tamanho que é disponibilizada causando desperdício de recurso de máquina ao se provisionar uma máquina com muito recurso para uma carga que solicita pouco recurso.
•	Resizing das máquinas virtuais, ou seja, redimensionamento das máquinas atuais para ajustar as cargas, evitando desperdício de recursos. Para isso existe a transferência de cargas de trabalho entre máquinas que não estão perto de sua alocação de recurso máxima a fim de desprovisionar máquinas desnecessárias. Exemplo, 2 máquinas iguais com uso de 30%, 1 máquina transfere as cargas pra outra ficando com 60% e 1 delas pode desligar.
•	Caso não existam VMs Spots disponíveis no momento da alocação de uma carga no Kubernetes, a carga é alocada numa VM normal, ainda sim garantindo alta disponibilidade.
Obs:
•	Modelo de contrato “Pay as you save”, fornece desconto líquido de aproximadamente 65% em relação a máquinas On Demand.
•	Caso não exista máquina spot para sua carga de trabalho será selecionada uma maquina regular.

## Tipos de Cargas
Recomendadas
•	Cargas de trabalho em que não é necessário alta disponibilidade. Exemplo: ambientes de DEV e QA. (Hoje as cargas de todos os projetos já estão em VMs Spot em DEV e QA).
•	Cargas de Airflow no geral, desde que as tasks não sejam muito longas e a ocorrência de possíveis retries e um pouco de atraso na DAG não seja crítico, o que é o teoricamente já esperado para cargas em batch.
•	Aplicações de Backend, Frontend, Jobs.
Não Recomendadas
Alguns tipos de cargas não são recomendadas para uso de Spot, aqui estão listadas elas com seus motivos:
•	Cargas críticas que exigem alta disponibilidade. Aumentar a quantidade de réplicas caso possível com antiafinidade pode ser uma alternativa para rodar em VM Spot.
•	Tasks muito longas no Airflow, acima de algumas horas. Quanto mais longa, maior o risco.
•	Bancos de dados não distribuídos (com apenas 1 replica): O resets do pod do banco devido a troca de máquina virtual pode causar indisponibilidade em todas as aplicações (caso sejam muitas e que precisem alta disponibilidade) que dependam de acesso ao banco.

## Possíveis Adequações
### Aumentar recursos subdimensionados
As VMs não spot utilizadas hoje são provisionadas com bastante recurso e isso permite sobra de recursos pra escalar e comportar cargas subdimensionadas (que usam mais recurso do que solicitam). Porém com VMs Spot, os tamanhos de VMs serão alocados de forma mais otimizada de acordo com a solicitação da carga, possivelmente com pouca sobra de recurso para escalar. Portanto os recursos das cargas devem estar configurados corretamente.

Se uma carga usar muito mais do que requisitar utlizando VM Spot há um grande risco da carga quebrar, pois na requisição inicial foi pedido uma quantidade de recurso, mas a carga precisa usar mais do que existe de recurso na VM em que foi alocada.

Para evitar isso é bom acompanhar o dashboard no grafana Recursos Cluster PRD - Namespace - Dashboards - Grafana (raizen.ai) em que mostra a diferença entre recurso solicitado e usado e fazer as correções necessárias.

### Aumentar recursos em cargas de longa duração
No caso de cargas em que a solicitação de recurso seja inversamente proporcional ao tempo de execução, é possível aumentar a solicitação de recursos para que a carga execute mais rápido e tenha menos risco de interrupção da VM Spot.

Obs: Nem sempre essa lógica se aplica diretamente para cargas que utilizam Spark sem que outras configurações do Spark sejam customizadas e otimizadas para este fim.


# Implementação
Kubernetes
Para configurar que um pod seja executado numa máquina Spot é necessário adicionar as seguintes configurações de nodeSelector e 
tolerations:

```
      nodeSelector:
        spot: 'true'
      tolerations:
      - effect: NoSchedule
        key: kubernetes.azure.com/scalesetpriority
        operator: Exists
```

A fim de automatizar que essas configurações sejam implementadas em todos os pods sem precisar alterar os códigos yamls de cada carga de trabalho foi utilizado a ferramenta Gatekeeper que faz a mutação das solicitações de criações de pod antes de serem executadas, assim conseguimos alterar as requisições adicionando essas configurações.
Exemplo:

Para que isso funcione é necessário apenas criar um label spot: 'true' no namespace onde esse comportamento é desejado.
Exemplo:

```
apiVersion: v1
kind: Namespace
metadata:
  name: prog
  labels:
    agentpool: 'spot'
```

## Restrict Scale Down
Para desabilitar o Resizing de máquinas em que certas cargas de trabalho estão provisionadas, a fim de proporcionar uma disponibilidade maior dessas aplicações pode-se adicionar a label no pod:
labels:
  spotinst.io/restrict-scale-down: 'true'
Carga elegíveis:
•	Pods de usuários dos ambientes de desenvolvimento para evitar restarts.
•	Banco de dados do Airflow de QA.
Airflow
Caso alguma task/dag precise executar em spot especificamente, porém outras não no mesmo namespace. Exemplo:
from kubernetes.client import models as k8s

```
executor_config={
    "pod_override": k8s.V1Pod(
        metadata=k8s.V1ObjectMeta(
            namespace="prog",
         ),
        spec=k8s.V1PodSpec(
            #service_account_name='xxxxxxxxxx'
            containers=[
                k8s.V1Container(
                    name="base",
                    image="xxxxxxxxxx",
                    resources=k8s.V1ResourceRequirements(
                        requests={
                            "memory": "1G", 
                            "cpu": 0.5,
                        },
                    ),
                )
            ],
            node_selector={"spot": "true"},
            tolerations=[
              k8s.V1Toleration(
                key="kubernetes.azure.com/scalesetpriority",
                operator="Exists",
                effect="NoSchedule"
              ),
              k8s.V1Toleration(
                key="spot",
                operator="Exists",
                effect="NoSchedule"
              )
            ],
        )
    )
}
```
