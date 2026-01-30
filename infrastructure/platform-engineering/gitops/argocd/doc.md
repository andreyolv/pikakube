https://github.com/argoproj/argo-cd
https://github.com/argoproj/argo-helm

sem helm chart para argocd core, só apply manual meio merda e comunidade cagando pra isso
https://github.com/argoproj/argo-helm/issues/1823

no limiting clusterResourceWhitelist to specific resource names
https://github.com/argoproj/argo-cd/issues/12208

ridiculo demais
https://github.com/argoproj/argo-cd/issues/5202
https://github.com/argoproj/argo-cd/issues/7437

kubectl port-forward svc/argocd-server -n argocd 8080:443

username: admin
password: 
kubectl get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo

install argocd cli
https://argo-cd.readthedocs.io/en/stable/cli_installation/#download-with-curl

github app credential to repo access
https://argo-cd.readthedocs.io/en/stable/user-guide/private-repositories/#github-app-credential

https://github.com/settings/apps/argocd-app-of-apps
https://github.com/settings/installations/<github-app-installation-id>

argocd repo add https://github.com/andreyolv/pikakube.git \
 --github-app-id xxxx \
 --github-app-installation-id xxxxx \
 --github-app-private-key-path argocd-app-of-apps.private-key.pem

argocd account list
argocd cluster list
argocd repo list
argocd app list

argocd helmrepository volume n tem igual flux 
argocd selfHeal: true no argo serio isso?
arquitetura de componentes doflux é melhor distribuida componentes por função
passar secrets nos values do flux é melhor