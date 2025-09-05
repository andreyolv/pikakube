Políticas de TAGs nos Resource Groups da Azure:
Preencher 2 Tags: RG_PoliticaCusto e ProjetoAnalytics

Quais possibilidades pra esses campos: 
RG_PoliticaCusto = ProjetoUnico, ProjetoCompartilhado, KubernetesCompartilhado, CentroCompartilhado
ProjetoAnalytics = ProjetoX, ProjetoY, ... KubernetesDEV, KubernetesQA, KubernetesPRD

Cenários / Exemplos:
1- Um RG é usado apenas por 1 projeto:
PoliticaCusto = ProjetoUnico
ProjetoAnalytics = Projeto1

2 - Um RG é usado para n projetos:
PoliticaCusto = ProjetoCompartilhado

resource A -> ProjetoAnalytics = Projeto1
resource B -> ProjetoAnalytics = Projeto2

Obs: Necessário tagear recurso a recurso com a tag específica do projeto de cada recurso.

3- Um RG é usado pelo AKS com dezenas de projetos dentro:
PoliticaCusto = KubernetesCompartilhado
ProjetoAnalytics = KubernetesDEV

Obs: divisão desse custo será feita com outras ferramentas.

4- Um RG é usado pelo centro inteiro. Ex: Datalake
PoliticaCusto = CentroCompartilhado