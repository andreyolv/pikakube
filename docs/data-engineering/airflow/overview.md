# Overview - Airflow no Kubernetes
## Introdução
O Apache Airflow é uma plataforma de orquestração de fluxo de trabalho de código aberto. Ele começou como um projeto interno na Airbnb em 2014 e foi lançado como código aberto em 2016 no Apache Software Foundation.
Aqui na Raízen utilizamos preferencialmente o Airflow para orquestração de tarefas, pois além de ser uma ferramenta poderosa, flexível e fácil de usar, ele também é altamente escalável quando executado em um ambiente Kubernetes.

## Arquitetura
O Airflow é composto por três componentes principais:
•	Webserver: Interface gráfica para gerenciamento de DAGs, execuções, logs, etc.
•	Scheduler: Responsável por agendar e executar as tarefas de acordo com as dependências definidas.
•	Executor: Responsável por executar as tarefas.
Além desses componentes, o Airflow também utiliza um banco de dados para armazenar metadados e logs das execuções e, no nosso caso, um DagProcessor para carregar as DAGs.
Todos esses componentes existem em pods separados no Kubernetes, o que permite que cada um deles seja escalado individualmente e, em alguns casos, possuam réplicas para garantir alta disponibilidade. É de responsabilidade da equipe de DataOps garantir que esses componentes estejam funcionando corretamente.

https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/dagfile-processing.html

https://airflow.apache.org/docs/apache-airflow/stable/installation/upgrading_to_airflow3.html

https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html

https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html

## DAGs
DAGs (Directed Acyclic Graphs) são a representação dos fluxos de trabalho no Airflow. Eles são compostos por tarefas (tasks), que são as unidades de execução, e são definidos em arquivos Python.
No Airflow, as DAGs são carregadas pelo DagProcessor e armazenadas no banco de dados. O Scheduler é responsável por verificar se as tasks de uma DAG estão prontas para serem executadas e, caso estejam, envia a execução para o Executor.

## Tasks
As tasks são as unidades de execução de uma DAG. Elas podem ser de diferentes tipos, como BashOperator, PythonOperator, etc., e são responsáveis por executar o código que realiza a tarefa.
Elas podem ser executadas em diferentes executores, como LocalExecutor, CeleryExecutor e KubernetesExecutor. No nosso caso, utilizamos o KubernetesExecutor, que as executa em pods no Kubernetes seguindo as configurações definidas no parâmetro executor_config da task.

# KubernetesExecutor
O KubernetesExecutor é um executor do Airflow que executa as tasks em pods no Kubernetes. Ele é altamente escalável e permite que as tasks sejam executadas em containers isolados, o que é ideal para ambientes de produção. Além disso, ele também suporta a execução de DAGs em namespaces diferentes, permitindo a separação de unidades de trabalho (como áreas, times, etc.).

Aqui na Raízen a imagem base utilizada para as tasks é a raizenanalyticsdev.azurecr.io/airflow-base , definida no repositório airzflow, sendo todas as tasks executadas em containers com imagens derivadas dessa base (e.g., a sparkzen). É importante salientar que no DagProcessor a imagem base é utilizada para carregar as DAGS, ou seja, dentro do arquivo python da DAG não é possivel utilizar métodos que dependam de bibliotecas não presentes na imagem base, sendo assim é altamente recomendado que os callables das tasks sejam definidos em arquivos separados e importados no arquivo da DAG via lazy-import ou com imports dentro da função.

Na definição da executor_config do KubernetesExecutor é necessário definir também o namespace onde as tasks serão executadas e os recursos que cada pod terá disponível. É importante que esses recursos sejam configurados de acordo com as necessidades de cada task afim de evitar problemas de recursos insuficientes ou ociosos. Exemplo de configuração:

```
executor_config = {
    "KubernetesExecutor": {
        "namespace": "sicle",
        "request_memory": "2Gi",
        "request_cpu": "1",
        "limit_memory": "4Gi",  # Optional
        "limit_cpu": "2",  # Optional
    }
}
```

O request de recursos segue a mesma lógica do Kubernetes, onde o request é o mínimo garantido para a task e o limit é o máximo que a task pode consumir. É importante que o request seja menor ou igual ao limit. Caso o limit não seja definido, o cluster irá fornecer recursos solicitados além do request, porém sem garantia de que a task não será interrompida na execução para realocação de recursos. Idealmente, o request de memória deve ser o mais próximo possível do consumo real máximo da task, porém o request de CPU pode ser mais próximo do consumo médio, visto ser um recurso flexível (capaz de ser alongado ou encurtado conforme a demanda).

Quando uma task precisa ser interrompida por falta de recursos ela recebe um comando de SIGTERM, que é capturado pelo Airflow e tratado de acordo com a política de retries definida. Em operações críticas, é recomendado que a task seja capaz de ser interrompida e retomada sem problemas, garantindo a integridade dos dados e a consistência da execução.

É importante não confundir o KubernetesExecutor com o KubernetesPodOperator. O KubernetesPodOperator é uma task específica do Airflow que executa um pod no Kubernetes, enquanto o KubernetesExecutor é o executor do Airflow que executa as tasks em pods no Kubernetes, ou seja, se você utilizar o KubernetesExecutor todas as tasks serão executadas em pods no Kubernetes, independentemente do tipo de task.

## DAG Import Errors
Toda vez que uma DAG é carregada pelo DagProcessor, o Airflow tenta importar o arquivo Python da DAG para verificar se a DAG foi definida corretamente. Caso ocorra algum erro de importação, a DAG não será carregada e o erro será registrado no topo do webserver. Os erros de importação mais comuns são:
•	ModuleNotFoundError: Alguma biblioteca utilizada no arquivo da DAG não está presente na imagem base. Para resolver esse erro é necessário mover a importação da biblioteca para o arquivo da task ou adicionar a biblioteca na imagem base. Esse exception pode aparecer também quando o arquivo analisado não é uma DAG, mas foi interpretado como tal. Para evitar esse tipo de erro utilize o arquivo .airflowignore para ignorar arquivos/pastas que não contém DAGs.
•	SyntaxError: Erro de sintaxe no arquivo da DAG. Para resolver esse erro é necessário corrigir o erro de sintaxe no arquivo da DAG. Preste atenção em erros de importação local (como caracteres especiais, espaços, etc. no nome do arquivo) e erro de indentação.
•	ImportError: Alguma dependência não foi encontrada ou algum módulo está quebrado. Esse erro diferencia-se do ModuleNotFoundError pelo fato do módulo estar presente, mas não ser importável.
•	KeyError: Em especial quando o erro é referente a uma variável do proprio Airflow (Variables, Conns, etc.), é possível que a variável não esteja definida no banco de dados do Airflow. Para resolver esse erro é necessário definir a variável no Airflow, porém é recomendado que essas variáveis sejam importadas apenas no arquivo da task, evitando que o banco de dados seja acessado toda vez que a DAG é carregada no DagProcessor.
•	AirflowClusterPolicyViolation: Erro de política de execução da DAG. Para resolver esse erro é necessário verificar se a DAG está configurada corretamente, se as dependências estão corretas e se os parâmetros de execução estão de acordo com a política de execução da DAG, disponível em Políticas do Airflow QA/PRD.

## Deploy
Nossas DAGs são armazenadas em repositórios Git e carregadas para o Airflow (pasta /dags existente em um Azure Storage) via Github Actions. O processo é automatizado e ocorre a cada push na branch main/qa do repositório ou de acordo com a configuração do workflow. É importante que apenas DAGs funcionais sejam enviadas para os ambientes de qualidade e produção afim de minimizar o risco de sobrecarga no DagProcessor, bem como evitar múltiplos deploys seguidos sem necessidade (hotfixes, etc.).

## FAQ (Geral)
Como faço para acessar o Airflow?
O Airflow é acessado via navegador, através do endereço https://airflow.qa.raizen.ai/ para o ambiente de qualidade e https://airflow-prd.raizen.ai/ para o ambiente de produção. Para acessar é necessário estar conectado à VPN da Raízen e possuir um usuário cadastrado no Airflow.

Como faço para criar um usuário no Airflow?
Para criar um usuário no Airflow é necessário acionar a equipe de Data Ops solicitando a criação de um usuário no Airflow. É necessário informar o nome completo, e-mail e o ambiente (QA ou PRD) onde o usuário será criado, bem como quais DAGs o usuário terá acesso.

Como faço para criar uma DAG no Airflow?
Para criar uma DAG no Airflow é necessário existir um repositório Git com a DAG e um arquivo de configuração de deploy. O deploy é feito via Github Actions e o arquivo de configuração deve conter as informações necessárias para o deploy da DAG no Airflow. A equipe de Data Ops é a responsável por construir o repositório padrão e o arquivo de configuração de deploy. 

## FAQ (KubernetesExecutor)
Minha task está falhando por falta de recursos.
Caso a task esteja falhando por falta de recursos (SIGTERM/SIGKILL), é necessário verificar se os recursos solicitados estão de acordo com as necessidades da task. Além disso, verifique se o consumo atual da task está dentro do esperado para a dimensão do processo e se não há vazamento de recursos (e.g., SparkSession com configurações de memória e cores muito acima do requisitado). No geral, é recomendado que cada task utilize no máximo 45Gi (limite da JVM para alocação de memória) e 8 CPUs, porém esses valores podem variar de acordo com a necessidade da task. Para verificar o consumo real da task utilize os 

## Dashboards do Grafana.
Grafana PRD
Grafana QA
Grafana DEV

Minha task aparece no Airflow, mas não está sendo executada.
Nos casos em que a task passa pelo scheduler mas não consegue ser alocada (fica queued ou up_for_retry), alguns cenários são possíveis:
•	Excesso de tasks: O cluster está com muitas tasks em execução e não consegue alocar novas. Nesse caso, é necessário aguardar a liberação de recursos para que a task seja executada. Verifique os pools de execução e a fila de tasks no Airflow.
•	Imagem contém erros: A imagem utilizada para a task contém erros e não consegue ser executada. Nesse caso, o container da task é criado e imediatamente destruído, gerando um erro no Airflow. Caso a imagem seja nova, verifique se esta foi construída corretamente e se a referência está correta no arquivo da DAG.

Aparece um aviso de OOMKilled na task.
O aviso de OOMKilled indica que a task foi interrompida por falta de memória. Isso pode ocorrer quando a task consome mais memória do que o limite definido. Para resolver esse problema, é necessário verificar o consumo de memória da task e ajustar o request e/ou limit de memória do executor.
A memória da task aumenta constantemente durante a execução até falhar.
Caso a memória da task aumente constantemente durante a execução, é possível que a task tenha um vazamento de memória. Isso pode ocorrer quando a task aloca memória e não libera, como em loops longos ou processos que mantém referências a objetos grandes. Para resolver esse problema, é necessário identificar o vazamento de memória e corrigir o código da task.
Mesmo com o request de CPU alto, a task não utiliza toda a CPU disponível.
Para utilizar um volume maior de CPU, é necessário que a task seja capaz de paralelizar o processamento. Ferramentas como Spark são capazes de utilizar múltiplos núcleos de CPU para processar os dados, porém é necessário que a task seja configurada corretamente para isso. Caso a task não seja capaz de paralelizar o processamento, é possível que a CPU fique ociosa durante a execução.
Links e Referências
Apache Airflow Docs
Apache Airflow GitHub

o	Template de Repositório
o	Imagem do Projeto
	Executorconfig


backup prd efs
