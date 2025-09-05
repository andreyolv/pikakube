--Zona DNS / PrivateLink
 configuração de Zona DNS Azure (privatelink), pulicação no DNS interno, publicação na VPN e liberação de porta para os seguintes endereços: 
name1234.dev.azuresynapse.net -> ip, porta 443 
name1234.sql.azuresynapse.net -> ip, porta 443 e 1443 (sql server) 
name1234-ondemand.sql.azuresynapse.net -> ip, porta 443 e 1443 (sql server)

--Firewall
IPs de origem:
AKS subnet dev
AKS subnet qa
AKS subnet prd

IPs de destino:
SUBNET de nome xxxxxx, bloco de ip yyyyyy
porta 1433

Portanto 3 regras de firewall para configurar.