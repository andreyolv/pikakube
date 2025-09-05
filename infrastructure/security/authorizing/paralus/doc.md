https://github.com/paralus/paralus
https://github.com/paralus/helm-charts

login
admin@paralus.local
kubectl logs -f --namespace paralus $(kubectl get pods --namespace paralus -l app.kubernetes.io/name='paralus' -o jsonpath='{ .items[0].metadata.name }') initialize | grep 'Org Admin default password:'
