https://github.com/kube-vip/kube-vip
https://github.com/kube-vip/helm-charts

docker network inspect kind -f '{{ range $i, $a := .IPAM.Config }}{{ println .Subnet }}{{ end }}'
