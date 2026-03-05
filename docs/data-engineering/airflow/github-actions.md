# GitHub Actions 

Motivação
Há um número muito grande de repositórios na organização raizen-analytics. O que torna a atualização das actions e a implementação de novas ferramentas de segurança nos fuxos de deploy de dags e construção de imagens em um trabalho exaustivo e demorado. Pensando nisso, decidiu-se centralizar as actions para que as manutenções necessárias fossem feitas em apenas um lugar. Assim, toda alteração pode ser feita de forma rápida, refletindo instantaneamente para todos os repositórios das organização.
O que são as Actions e onde encontrá-las?
As actions são ações realizadas nos workflows dos repositórios, presente nos arquivos YAML contidos na pasta “.github/workflows”.

Observação importante
No exemplo mostrado, usa a criação de uma nova tag como padrão. Esse tipo de gatilho é comum em repositórios que utilizam o Airflow. Em repositórios streamlit, o gatilho geralmente é um push na main ou na release, igual a action de deploy de dags.

