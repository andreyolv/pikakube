# Kubernetes

- Nós em status NotReady por longo períogo (geralmente estouro de memória, por isso importante executor_config no airflow setando recursos)
- Evicção de pods por OOM / disk pressure
- Falha no autoscaling de VMs pelo Karpenter
- Falha em upgrade de cluster
- Falha em upgrade de node pool
- Imagem de container não baixa
- Imagem de container não encontrada
- Falha github actions self hosted
- Falha em sincronizar segredos do vault no kubernetes
