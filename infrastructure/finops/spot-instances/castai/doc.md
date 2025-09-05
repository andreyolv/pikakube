https://github.com/castai/helm-charts

curl -H "Authorization: Token XXXXXXXXXXXXXXXXX" "https://api.cast.ai/v1/agent.yaml?provider=aks" | kubectl apply --dry-run=client -f - -o yaml> castai.yaml
