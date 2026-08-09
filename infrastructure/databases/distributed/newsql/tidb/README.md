https://github.com/pingcap/tidb
https://github.com/pingcap/tidb-operator

install crds before

kubectl create -f https://raw.githubusercontent.com/pingcap/tidb-operator/v1.6.1/manifests/crd.yaml --dry-run=client -o yaml | \
kubectl-slice --template '{{.kind | lower}}/{{.metadata.name | replace ".pingcap.com" ""}}.yaml' --output-dir .
