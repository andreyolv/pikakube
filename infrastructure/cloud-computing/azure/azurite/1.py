from azure.storage.blob import BlobServiceClient

# Conexão com o emulador de Blob Storage
connection_string = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

container_name = "pikakube"

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

container_client = blob_service_client.get_container_client(container_name)

if not container_client.exists():
    container_client.create_container()
    print(f"Contêiner '{container_name}' criado com sucesso!")
else:
    print(f"Contêiner '{container_name}' já existe.")

print("\nLista de contêineres disponíveis:")
for container in blob_service_client.list_containers():
    print(f"- {container['name']}")
