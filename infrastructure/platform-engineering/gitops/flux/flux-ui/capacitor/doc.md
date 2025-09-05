https://github.com/gimlet-io/capacitor

helmrelease não funciona pq carregar arquivo readme.md dentro do pacote https://github.com/gimlet-io/capacitor/tree/main/deploy/k8s
portanto usar Kustomization como sugere documentação

kubectl -n flux-system port-forward svc/capacitor 9000:9000

consigo ver via cli facilmente tudo que tem no dashboard, meio inútil