# !pip install azure-identity azure-keyvault-keys

from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

tenant_id = "xxxxxxxx"
client_id = "xxxx"
client_secret = "xxxxxxx"

key_vault_url = "https://name.vault.azure.net/"

credential = ClientSecretCredential(tenant_id=tenant_id, 
                                    client_id=client_id, 
                                    client_secret=client_secret
                                   )

client = SecretClient(vault_url=key_vault_url,
                      credential=credential
                     )

secrets = client.list_properties_of_secrets()

for secret_properties in secrets:
    secret_name = secret_properties.name
    secret = client.get_secret(secret_name)
    print(f"Nome do segredo: {secret_name}, Valor: {secret.value}")