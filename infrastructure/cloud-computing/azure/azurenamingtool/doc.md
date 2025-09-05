https://github.com/mspnp/AzureNamingTool/wiki/Run-as-a-Docker-Image

baixar release e extrair aqui, não tem imagem oficial que merda
https://github.com/mspnp/AzureNamingTool/issues/125

docker build -t azurenamingtool .
docker run -d -p 8080:80  azurenamingtool

https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming
