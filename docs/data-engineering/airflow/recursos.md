# Monitoramento de Recursos de Tasks do Airflow pelo Grafana
•	Introdução
•	Recursos do Kubernetes 
o	Recursos de Containers
o	Recursos de VMs (Máquina Virtual)
•	Configurações de Recursos no Apache Airflow
•	Monitoramento de Métricas de Recursos 
o	Dashboard
o	Métricas do Prometheus
o	Comportamento de Recursos no Contexto de Dados
•	Recursos Inadequados 
o	Memória e CPU Superdimensionados
o	Memória sobredimensionada
o	CPU sobredimensionada
•	Resumo 
o	Memória (Gi)
o	CPU (vCPU)

## Introdução
Ao executar cargas de trabalho no Kubernetes, cada aplicação é empacotada em Pods, que por sua vez contêm containers. Para garantir uma utilização eficiente da infraestrutura, é boa prática definir os recursos (CPU e memória) que cada container pode utilizar.
Essa definição é fundamental para:
•	Garantir a estabilidade e performance da aplicação.
•	Evitar desperdício de recursos.

## Recursos do Kubernetes
### Recursos de Containers
No Kubernetes, existem dois tipos principais de configurações de recursos por container:
requests (solicitação de recurso)
•	É a quantidade mínima garantida de CPU/memória que o container terá disponível.
•	O Kubernetes usa esse valor para decidir em qual nó alocar o Pod.
limits (limite de recurso)
•	É a quantidade máxima de CPU/memória que o container pode utilizar.
•	O container não pode ultrapassar esse valor. Se tentar, pode ter cpu estrangulada (throttled) ou até encerrado (OOMKilled) no caso da memória.
⚠️ Se os limits não forem definidos, o container poderá usar até o limite da máquina virtual em que está alocado, o que pode impactar outras aplicações no mesmo nó.
Os valores de requests são importantes para que a carga seja alocada numa VMs com recurso necessário solicitado.

### Recursos de VMs (Máquina Virtual)
Cada Pod é executado em uma VM (nó do cluster), que também possui seus próprios limites físicos de CPU e memória. Se um container tentar utilizar mais do que o disponível na VM e não houver limits definidos, ele pode ser encerrado ou causar instabilidade no cluster.

## Configurações de Recursos no Apache Airflow
No Airflow, cada Task é executada em um Pod, o que permite isolar e controlar os recursos utilizados por execução.
Formas de configurar os recursos (executor_config):
KubernetesExecutor
•	Forma mais antiga e ainda amplamente utilizada.
•	Ainda suportada, mas será descontinuada futuramente (sem data definida).
Exemplo:
executor_config = {
    'KubernetesExecutor': {
        'image' : 'raizenanalyticsdev.azurecr.io/fenix-airflow',
        'namespace': 'dataops-airflow',
        'request_memory' : '100Mi',
        'request_cpu': '0.1'
        'limit_memory': '1.5Gi',
        'limit_cpu': '1'
    }
}

...

    task1 = PythonOperator(
        task_id='task_1',
        python_callable=task1,
        executor_config=executor_config
    )
pod_override
•	Forma mais moderna, baseada em PodOverride.
Exemplo:
from airflow.sdk import dag, task
from kubernetes.client import models as k8s

k8s_resource_requirements = k8s.V1ResourceRequirements(
   requests={"cpu": 0.5, "memory": "1Gi"},
   limits={"cpu": "1","memory": "2Gi"}
)

executor_config={
   "pod_override": k8s.V1Pod(
       metadata=k8s.V1ObjectMeta(namespace="dataops-airflow"),
       spec=k8s.V1PodSpec(
           containers=[
               k8s.V1Container(
                   name="base",
                   resources=k8s_resource_requirements,
               )
           ],
       )
   )
}

...

def my_dag():
    @task(executor_config=executor_config)
    def task1():
        print("Running task 1")
        time.sleep(60)

## Monitoramento de Métricas de Recursos
O acompanhamento do consumo de recursos é feito através de um dashboard no Grafana de produção, alimentado por métricas coletadas pelo Prometheus.

### Dashboard
•	CPU e Memória requisitadas vs. utilizadas ao longo do tempo
Permite entender o comportamento da carga em tempo real e identificar gargalos ou desperdícios.
•	Visão segmentada por namespace
Cada projeto Airflow possui um namespace exclusivo no Kubernetes. O dashboard permite selecionar o namespace desejado e visualizar apenas os Pods daquele projeto.
•	Diagnóstico por Task individual
Cada execução de Task no Airflow sobe como um Pod. O dashboard apresenta os recursos consumidos por cada Pod ao longo da execução.
🔍 Primeiro passo:
Selecione o namespace do seu projeto no filtro superior do dashboard para restringir a visualização apenas aos Pods relevantes.
Links dos Grafanas
•	DEV: Recursos Cluster Dev - Namespace - Dashboards - Grafana
•	QA: Recursos Cluster QA - Namespace - Dashboards - Grafana
•	PRD: Recursos Cluster PRD - Namespace - Dashboards - Grafana

### Métricas do Prometheus
As métricas utilizadas neste dashboard são expostas pelo Prometheus e coletadas do cluster Kubernetes. As principais métricas utilizadas no painel são:
Métrica Prometheus	Descrição
kube_pod_container_resource_requests{resource="memory"}	Quantidade de memória requisitada (requests) por container
kube_pod_container_resource_requests{resource="cpu"}	Quantidade de CPU requisitada (requests) por container
container_memory_working_set_bytes	Memória efetivamente utilizada pelo container
container_cpu_usage_seconds_total	CPU efetivamente utilizado pelo container

Como o gráfico funciona?
O gráfico apresentado no dashboard faz o cálculo da diferença entre o recurso requisitado e o recurso usado ao longo do tempo:
Memory (Request - Usage) = kube_pod_container_resource_requests{resource="memory"} - container_memory_working_set_bytes
Exemplo:
(imagem)

CPU (Request - Usage) = kube_pod_container_resource_requests{resource="cpu"} - container_cpu_usage_seconds_total
Exemplo:
(imagem)

Essa diferença é apresentada no eixo Y, e o tempo no eixo X.
Dessa forma:
•	Valores positivos indicam que a carga usou menos do que o requisitado (possível superdimensionamento).
•	Valores negativos indicam que a carga usou mais do que o requisitado (possível subdimensionamento, risco de OOM (memória) ou throttling (cpu)).
(priorização)
(quebra por memória depende tamanho da sobre na máquina x alocação das máquinas são feitas dinamicamente e não dá pra saber antecipadamente em qual VM de qual tamanho carga é alocada, faz parte de eficience do kubernetes essa alocação de cargas)

### Comportamento de Recursos no Contexto de Dados
A quantidade de recursos consumidos por uma carga — especialmente em workloads de processamento de dados — pode variar bastante ao longo do tempo durante uma execução e também entre diferentes execuções.

Por isso, o ideal é que o mínimo da diferença entre o recurso requisitado e o utilizado seja próximo de zero ou ligeiramente acima de zero, garantindo uma margem de segurança.
Exemplo:
(imagem)

Não existe um "número mágico" para essa margem. Ela depende do tipo de processamento, do comportamento histórico da carga e da infraestrutura utilizada.
⚠️ Importante: Use os dados do dashboard como referência e sempre analise execuções múltiplas antes de ajustar recursos. Uma única execução fora da curva pode não justificar um ajuste imediato.

Levando em consideração a quantidade de cargas que estão muito fora desse intervalo e são prioritárias em questão de ajuste, podemos considerar razoável:

## Recursos Inadequados
### Memória e CPU Superdimensionados
O que é?
Quando a quantidade de recurso solicitada (requests) é muito maior do que o realmente utilizado.
Como identificar?
Diferença positiva grande no gráfico (recurso requisitado muito acima do usado).
Consequência:
•	Recursos ociosos consumindo capacidade do cluster.
•	Aumento desnecessário de custo.
Sugestão:
Reduzir os valores de requests para memória e/ou CPU, com base na análise histórica de uso.
Exemplo:
(imagem)

### Memória sobredimensionada
O que é?
Quando a memória requisitada (requests.memory) não é suficiente para a execução da carga e o kubernetes escala verticalmente o recurso usado de memória .
Como identificar?
Diferença negativa no gráfico. Ou seja, o uso de memória ultrapassa o que foi pedido.
Consequência:
•	O Pod pode ser alocado em uma VM com memória insuficiente.
•	Alto risco de ser interrompido por OOM (Out of Memory).
•	Possível falha na execução da Task.
Quanto mais negativo o valor, maior a probabilidade da carga ser interrompida.
Sugestão:
Aumentar a memória requisitada (requests.memory), com base no uso observado e com uma margem segura.
Exemplo:
(imagem)

### CPU sobredimensionada
O que é?
Quando a CPU requisitada (requests.cpu) não é suficiente para a execução da carga e o kubernetes escala verticalmente o recurso usado de cpu.
Como identificar?
Diferença negativa ou picos frequentes de uso acima do request.
Consequência:
•	A carga pode ser executada com lentidão (baixa performance).
•	Eventualmente, pode haver throttling (contenção de CPU).
Não há risco de interrupção do Pod, mas sim de gargalo e aumento no tempo de execução.
Sugestão:
Aumentar a CPU requisitada (requests.cpu) para evitar gargalos, especialmente em tarefas críticas ou com tempo sensível.
Exemplo:
(imagem)

## Resumo
### Memória (Gi)
Entre -x e +x Gi:
Considerada uma faixa razoável, com boa margem de segurança e baixo risco de interrupções por OOM (Out of Memory).
Acima de +x Gi:
Indica possível superdimensionamento e potencial de otimização.
Abaixo de -x Gi:
Risco elevado de OOM. Carga pode estar sendo executada em nó com recursos insuficientes.

### CPU (vCPU)
Entre -y e +y vCPU:
Faixa aceitável. Equilíbrio entre segurança e eficiência.
Acima de +y vCPU:
Pode indicar superdimensionamento. Avaliar histórico e comportamento da carga.
Abaixo de -y vCPU:
Sinal de subdimensionamento, com risco de throttling e lentidão. Verificar performance da task.
