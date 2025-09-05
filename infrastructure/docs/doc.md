# ADR
https://github.com/joelparkerhenderson/architecture-decision-record

https://github.com/joelparkerhenderson/architecture-decision-record/tree/main/locales/en/examples

legais, mas desnecessário. simplicidade, oq importa são informações, não formato e ferramenta
https://github.com/thomvaill/log4brains
https://github.com/adr/madr

# API
https://github.com/OAI/OpenAPI-Specification
https://github.com/asyncapi/spec
https://github.com/event-catalog/eventcatalog
https://github.com/swagger-api/swagger-ui
https://github.com/Redocly/redoc

# Diagrams
https://github.com/mingrammer/diagrams
https://github.com/mermaid-js/mermaid
https://github.com/philippemerle/KubeDiagrams
https://github.com/HariSekhon/Kubernetes-configs
https://github.com/HariSekhon/Diagrams-as-Code
https://github.com/awslabs/diagram-as-code

# host documentation:
-github pages
-https://github.com/readthedocs/readthedocs.org -> for open source packages 
-confluence https://github.com/Workable/confluence-docs-as-code

# diretrizes de documentação:
-plano/rotina de atualização de ferramentas e ter histórico documentado
-tudo q apresentar tem q documentar.
-documentação externa (para terceiros usarem, como faz etc)
-documentação interna (para o time)
-documentar procedimentos (atualização de airflow, backup velero, atualizar ambiente dev)
-documentar motivações de escolhas de arquitetura (adr)
-documentar regras de negócio
-documentar problemas frequentes FAQ (ex: airflow não sobe o pod)
-documentar incidentes e resolução
-documentar arquitetura de referencia / comitê arquitetura TI, documentação e padronização
-apresentar eventualmente as coisas em hubs pra reforçar conhecimento

```mermaid
flowchart LR
  A --> B
```


Status: [proposed | rejected | accepted | deprecated | … | superseded by ADR-0005]
Deciders: [list everyone involved in the decision]
consulted: list everyone whose opinions are sought
Date: [YYYY-MM-DD when the decision was last updated]
context/problema/necessidade
requisitos/escopo
considered options / o pq já elimina algumas facilmente exemplo, argocd e flux apenas pq não tem mais nenhuma ferramenta com maturidade
-options
- pros and cons
poc
decision/solution
justificativa
-consequences / debito técnico

planning agile, quebrar atividades
- cronograma
- comunicado impacto envolvidos

projeto/solução (com identificador do projeto)
- introdução
- infraestrutura
- configurações
- segurança
- monitoramento
- redes
- resiliência
- gestão de custo
- metadados (repositório, recurso cloud, etc)
- casos de uso (quando usar e quando não usar)
- operação/procedimentos comuns no dia a dia, tutoriais, pra facilitar novos integrantes, manuntenção, atualização etc
- apresentação da solução fim a fim, tranfer knowledge
- aprendizados, boas práticas, erros frequentes, faq, postmortem
- referencias


