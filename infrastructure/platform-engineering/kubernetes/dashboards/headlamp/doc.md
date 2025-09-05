https://github.com/headlamp-k8s/headlamp
https://github.com/headlamp-k8s/plugins

kubectl -n headlamp get secret headlamp-admin-token -o jsonpath='{.data.token}' | base64 -d

legal, mas olha essa merda 
https://github.com/headlamp-k8s/headlamp/issues/2385
pra limitar por namespace é uma bosta, só funciona com ClusterRole e ClusterRolebinding

oidc aks
https://github.com/kubernetes-sigs/headlamp/issues/2480
