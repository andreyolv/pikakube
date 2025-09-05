https://github.com/datacontract/datacontract-cli
https://github.com/datacontract/datacontract-specification
https://github.com/datacontract/datacontract-editor

pip install datacontract-cli[deltalake]
pip install datacontract-cli[kafka]
pip install datacontract-cli[postgres]
pip install datacontract-cli[s3]

datacontract init --template xxxxx

--github actions
datacontract lint (deixar arquivo datacontract.yaml na raiz do repositório)
datacontract test --server (dependendo da branch mudar server pra validação) 
        (como contrato conecta com o data source? spn? variaveis d ambiente?)
        (onde setar variaveis de ambiente? no github actions?)
        (se tiver vários SPNS no repositório? como fazer?)
        https://github.com/chgl/datacontract-cli/tree/main/datacontract/engines/soda/connections

como unir com monitoring e alertas no airflow?

https://github.com/datacontract/datacontract-cli?tab=readme-ov-file#best-practices

podemos adicionar campos no yaml q não quebra no lint, bom pra campos customs