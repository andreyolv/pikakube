TOKEN=$(kubectl get secret $(kubectl get sa default -o jsonpath="{.secrets[0].name}") -o jsonpath="{.data.token}" | base64 --decode)
API_SERVER_ENDPOINT=xxxxxxxxxxxx
NAMESPACE=dev-space-test

curl -k -H "Authorization: Bearer $TOKEN" https://$API_SERVER_ENDPOINT/api/v1/namespaces/$NAMESPACE/pods
