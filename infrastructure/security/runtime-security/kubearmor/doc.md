https://github.com/kubearmor/KubeArmor

kubectl create deployment nginx --image=nginx
POD=$(kubectl get pod -l app=nginx -o name)

kubectl exec -it $POD -- bash -c "apt update && apt install masscan"
