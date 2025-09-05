from azure.storage.blob import BlobServiceClient

connection_string = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

container_name = "pikakube"
blob_path = "gold/project1/flights.csv"

local_file_path = "flights.csv"

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

if not container_client.exists():
    print(f"Contêiner '{container_name}' não encontrado. Certifique-se de criá-lo antes de fazer upload.")
else:
    blob_client = container_client.get_blob_client(blob_path)
    with open(local_file_path, "rb") as file:
        blob_client.upload_blob(file, overwrite=True)
    print(f"Arquivo '{local_file_path}' enviado com sucesso para '{blob_path}' no contêiner '{container_name}'.")
