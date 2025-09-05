k port-forward service/vault 8200
export VAULT_ADDR="http://127.0.0.1:8200"
vault operator init
salve as keys e token
vault status
vault operator unseal (3x)
vault login (pass token)
vault secrets enable -path=andreyolv kv
vault kv put andreyolv/senha palavra1=giropops palavra2=strigus
vault kv get andreyolv/senha
vault policy write mypolicy mypolicy.hcl
vault token create -policy="mypolicy"
salvar token
Para logar na UI, acessar o pod vault-o e executar os comandos para criar usuário: 
k port-forward svc/vault-ui 8210:8200
Method Token e passar Initial Root Token