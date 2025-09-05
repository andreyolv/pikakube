https://github.com/helm/helm

https://github.com/helm/chart-releaser

https://github.com/Masterminds/sprig

https://github.com/helm/helm-mapkubeapis

kubectl get secrets sh.helm.release.v1.airflow.v1 -o jsonpath='{.data.release}' | base64 -d | base64 -d | gzip -d

procurar quais charts existem em um helm repository
helm repo add strimzi https://strimzi.io/charts/
helm search repo strimzi
helm search repo strimzi/strimzi-drain-cleaner --versions

listar helmreleases instalados manualmente
helm list -A

pegar values de helmrelese instalado manualmente
helm get values retina -n kube-system

# Manual Upgrade
helm upgrade --install airbyte airbyte/airbyte --version 1.8.1 -n airbyte -f values-new.yaml --debug
