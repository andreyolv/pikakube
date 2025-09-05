https://github.com/loft-sh/vcluster

curl -L -o vcluster "https://github.com/loft-sh/vcluster/releases/download/v0.24.1/vcluster-linux-amd64" && sudo install -c -m 0755 vcluster /usr/local/bin && rm -f vcluster

vcluster --version

vcluster create my-vcluster --namespace team-x
kubectl get namespaces # See the namespaces of your virtual cluster
...
vcluster disconnect
vcluster delete my-vcluster --namespace team-x

