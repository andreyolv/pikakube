https://github.com/kumahq/kuma

kubectl port-forward svc/demo-app -n kuma-demo 5000:5000
kubectl port-forward svc/kuma-control-plane -n kuma 5681:5681
http://127.0.0.1:5681/gui/