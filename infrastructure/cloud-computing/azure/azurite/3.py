from azure.storage.blob import BlobServiceClient
import pandas as pd
from io import StringIO

connection_string = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

container_name = "pikakube"
blob_path = "gold/project1/flights.csv"

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path)

print(f"Fazendo download do arquivo '{blob_path}' do contêiner '{container_name}'...")
blob_data = blob_client.download_blob().readall()

csv_content = blob_data.decode("utf-8")
df = pd.read_csv(StringIO(csv_content))

print("\nConteúdo do arquivo CSV como DataFrame:")
print(df)
