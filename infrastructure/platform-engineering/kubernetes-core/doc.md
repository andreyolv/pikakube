https://aws.github.io/aws-eks-best-practices/

https://github.com/kubernetes/kubernetes
https://github.com/kubernetes/kubectl

https://github.com/kubernetes/autoscaler
https://github.com/kubernetes/community

https://github.com/dotdc/grafana-dashboards-kubernetes
https://github.com/kubernetes-client/python
https://github.com/kubernetes-sigs/kui
https://github.com/kubernetes-sigs/secrets-store-csi-driver
https://github.com/kubernetes/pod-security-admission
https://github.com/kubernetes/registry.k8s.io
https://github.com/container-storage-interface/spec

https://github.com/GoogleCloudPlatform/kubectl-ai

https://github.com/kubernetes/enhancements

kubectl delete pod <pod> --grace-period=0 --force

kubectl exec -it <pod> -c vscode -- df -h
kubectl exec -it <pod> -c vscode -- rm -rf /home/coder/airflow/logs/

kubectl delete pod $(kubectl get pods | grep 'connect-cluster-portal' | awk '{print $1}')
kubectl delete crd $(kubectl get crds | grep '.gatekeeper\.sh' | awk '{print $1}')

kubectl delete pod kafka-mtolv-zookeeper-0 --grace-period=0 --force

kubectl get apiservice|grep False
kubectl delete apiservice <apiservice name>

# Force delete namespace
kubectl delete pod prog-baseline-validator-motor-shxzt-9pzdk --grace-period=0 --force
kubectl patch pod prog-baseline-validator-motor-shxzt-9pzdk -p '{"metadata":{"finalizers":[]}}' --type=merge

kubectl get pod prog-baseline-validator-motor-shxzt-9pzdk -o json > pod.json
kubectl replace --raw "/api/v1/namespaces/prog/pods/prog-baseline-validator-motor-shxzt-9pzdk/finalize" -f pod.json

kubectl get namespace <TERMINATING_NAMESPACE> -o json | jq '.spec = {} | .metadata.finalizers = []' > tempfile.json && \
kubectl replace --raw "/api/v1/namespaces/<TERMINATING_NAMESPACE>/finalize" -f ./tempfile.json && \
rm -f tempfile.json

kubectl get pods --field-selector status.phase=Running

kubectl drain aks-d64z1-39255961-vmss00000k --ignore-daemonsets --delete-local-data
se drain não funciona e fica travado infinito deletar todos os pods mesmo
'''
kubectl get pods -A --field-selector spec.nodeName=aks-spot-9d8s2 \
  -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name' --no-headers | \
  while read namespace name; do
    echo "Forçando delete do pod $name no namespace $namespace"
    kubectl delete pod "$name" -n "$namespace" --grace-period=0 --force
  done

'''

kubectl delete node aks-d64z1-39255961-vmss00000k

https://knowledge.broadcom.com/external/article/298697/how-to-evenly-distribute-pods-across-a-t.html
 
k logs -l component=scheduler -c scheduler -f --max-log-requests 8 --tail 100 | grep TOR-headshot-reprocessing