https://github.com/argoproj/argo-workflows
https://github.com/argoproj/argo-helm

https://argo-workflows.readthedocs.io/en/latest/security/

ARGO_TOKEN="Bearer $(kubectl get secret argo-workflow-ui-service-account-token -o=jsonpath='{.data.token}' | base64 --decode)"
echo $ARGO_TOKEN

meio merda hein
https://github.com/argoproj/argo-workflows/discussions/13257

https://github.com/argoproj/argo-workflows/tree/main/examples