https://github.com/spotinst/charts

Tipos de Máquinas Virtuais
Todas as cargas de trabalho que rodam nas instâncias de cluster kubernetes são executadas em máquinas virtuais em um cloud provider, no nosso caso a Azure.

Em relação a forma de pagamento, existem basicamente 3 classes de máquinas virtuais nos cloud providers:

On Demand: Paga-se conforme o uso. Recomendado para quando não existe previsibilidade do uso contínuo das máquinas.

Reserva de Instância: Paga-se antecipadamente pela reserva de instâncias específicas. Recomendado para quando existe previsibilidade de uso contínuo das máquinas. Fornece descontos aproximados entre 30 a 40% em relação a máquinas On Demand.

Spot: São sobras de máquinas sem utilização pelo cloud provider. Fornece descontos de aproximadamente 90% em relação a máquinas On Demand. E não possuem SLA, pois o cloud provider pode interromper as máquinas a qualquer momento.

 

Spot Ocean
Características especificas que a solução Spot Ocean para máquinas spot oferece:

Monitora famílias de máquinas virtuais mais baratas e com menor probabilidade de interrupção, a fim de garantir maior disponibilidade mesmo sendo uma máquina spot, melhorando relação custo benefício. Sem a Spot Ocean, o cloud provider pode demorar alguns minutos para realocar a carga interrompida. A Ocean consegue prever quando uma máquina será desprovisionada e solicita criação de outra com antecedência.

Alocação heterogênea de classes de máquinas virtuais evitando desperdício de recursos. Ou seja, é possível subir uma máquina com o tamanho ideal para a carga que deseja-se alocar no momento. Ao contrário de máquinas de reserva de instâncias em que é sempre a mesma classe de máquina com mesmo tamanho que é disponibilizada causando desperdício de recurso de máquina ao se  provisionar uma máquina com muito recurso para uma carga que solicita pouco recurso. 

Resizing das máquinas virtuais, ou seja, redimensionamento das máquinas atuais para ajustar as cargas, evitando desperdício de recursos. Para isso existe a transferência de cargas de trabalho entre máquinas que não estão perto de sua alocação de recurso máxima a fim de desprovisionar máquinas desnecessárias. Exemplo, 2 máquinas iguais com uso de 30%, 1 máquina transfere as cargas pra outra ficando com 60% e 1 delas pode desligar.

Obs:

Modelo de contrato “Pay as you save”, fornece desconto líquido de aproximadamente 65% em relação a máquinas On Demand.

Caso não exista máquina spot para sua carga de trabalho será selecionada uma maquina regular.

 

Tipos de Cargas
Recomendadas
Cargas de trabalho em que não é necessário alta disponibilidade. Exemplo: ambientes de DEV e QA. (Hoje as cargas de todos os projetos já estão em VMs Spot).

Cargas de Airflow no geral.

Aplicações de Backend, Frontend, Jobs.

Não Recomendadas
Alguns tipos de cargas não são recomendadas para uso de Spot, aqui estão listadas elas com seus motivos:

Tasks muito longas no Airflow, acima de algumas horas. Quanto mais longa, maior o risco.

Bancos de dados não distribuídos (com apenas 1 replica): O resets do pod do banco devido a troca de máquina virtual pode causar indisponibilidade em todas as aplicações (caso sejam muitas e que precisem alta disponibilidade) que dependam de acesso ao banco. 

 

Possíveis Adequações
Recursos no KubernetesExecutor mal configurados
As VMs não spot utilizadas hoje são provisionadas com bastante recurso e isso permite sobra de recursos pra escalar e comportar cargas mal dimensionadas que usam mais recurso do que solicitam. Porém com VMs Spot, o tamanho das VMs será alocado de forma mais otimizada de acordo com a solicitação da carga. Portanto os recursos das cargas devem estar configurados corretamente.

Se uma carga usar muito mais do que requisitar utlizando VM Spot há um grande risco da carga quebrar, pois na requisição inicial foi pedido uma quantidade de recurso, mas a carga precisa usar mais do que existe de recurso na VM em que foi alocada.

Para evitar isso é bom acompanhar o dashboard no grafana xxxxxxxx em que mostra a diferença entre recurso solicitado e usado e fazer as correções necessárias.

Solicitação de Adição do Namespace a Spot
Da parte do projeto e responsável técnico do namespace não é necessário configurar nada. 

Deve-se apenas abrir um card ao final do backlog de DataOps em:


com as seguintes informações:

Namespace: Qual o nome do namespace no kubernetes que deseja adição em VM Spot.

Reponsável técnico pelo namespace: Analytics Engineer, Data Engineer ou Data Scientist responsável por acompanhar a execução das cargas no namespace durante 1 semana e relatar DataOps caso tenha algum problema.

Caso particular: Por padrão o namespace inteiro será adicionado para execução em VM Spot. Caso exista alguma exceção em que deseja adicionar apenas algumas cargas do namespace em VM Spot, porém outra não, explicar o caso. 

Exemplo
Nome do Card: VM Spot/PRD - Adicionar namespace xyz

Definition of Done:

Namespace: xyz

Responsável técnico: xyz

Caso particular: Não

 