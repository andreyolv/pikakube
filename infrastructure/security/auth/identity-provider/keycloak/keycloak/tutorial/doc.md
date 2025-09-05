k port-forward svc/keycloak-http 8080:80

# Criar realm
pela UI dar name 'Analytics'

# Configurar Github como Identity Provider
https://www.keycloak.org/docs/latest/server_admin/#_github
No Keycloak clicar em Identity Providers e Github, copiar Redirect URL.

No Github acessar https://github.com/settings/developers e preencher:
Application name: keycloak-integration
Homepage URL: http://127.0.0.1:8080/auth/realms/Analytics
Authorization callback URL: http://127.0.0.1:8080/auth/realms/Analytics/broker/github/endpoint (colar Redirect URI)
Copiar Client ID e Client Secret do Github para o Keycloak
Client ID: 5ba963f0a583b9fbe157
Client Secret: b3d875859e0e5286f4473ba5dd9d4580fb3064c1

Para testar acessar: http://127.0.0.1:8080/auth/admin/Analytics/console/

https://min.io/docs/minio/kubernetes/gke/operations/external-iam/configure-keycloak-identity-management.html
curl -d "client_id=minio" \
     -d "client_secret=U0HJ8kFW2wOgmD5p2y0hUKKOwmdHPBKL" \
     -d "grant_type=password" \
     -d "username=andrey" \
     -d "password=andrey" \
     http://127.0.0.1:8080/auth/realms/Analytics/protocol/openid-connect/token