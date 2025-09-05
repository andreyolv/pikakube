https://github.com/fission/fission

before apply helmrelease apply crds
kubectl create -k "github.com/fission/fission/crds/v1?ref=v1.20.5" --dry-run=client -o yaml | kubectl-slice -f - -o ./crds

sem exemplos pra kubernetes