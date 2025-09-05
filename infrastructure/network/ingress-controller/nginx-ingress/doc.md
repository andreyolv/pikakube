https://github.com/nginx/kubernetes-ingress

kubectl create -f "https://raw.githubusercontent.com/nginx/kubernetes-ingress/v4.0.0/deploy/crds.yaml" --dry-run=client -o yaml | kubectl-slice -f - -o ./crds --template '{{.spec.names.plural}}.yaml'

não precisa aplicars os crds antes não, comi bola