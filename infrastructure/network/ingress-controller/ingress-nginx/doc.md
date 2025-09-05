https://github.com/kubernetes/ingress-nginx

values para kind:
https://github.com/kubernetes/ingress-nginx/blob/main/hack/manifest-templates/provider/kind/values.yaml
https://github.com/kubernetes/ingress-nginx/blob/main/deploy/static/provider/kind/deploy.yaml

GERAR CERTIFICADOS:
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt
openssl req -x509 -newkey rsa:4096 -sha256 -nodes -keyout tls.key -out tls.crt -subj "/CN=seudominio.com" -days 365


CONVERTER ARQUIVO DE FORMATO PFX:
openssl pkcs12 -in [yourfile.pfx] -chain -clcerts -nokeys -out tls.crt
openssl pkcs12 -in [yourfile.pfx] -nocerts -out encrypted-key.key
openssl rsa -in encrypted-key.key -out tls.key

kubectl create secret tls [secret-name] --cert=tls.crt --key=tls.key --dry-run=client -o yaml > secret-name.yaml

https://kubernetes.github.io/ingress-nginx/examples/auth/oauth-external-auth/
https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#rate-limiting

certificate signed by unknown authority ->
kubectl delete -A ValidatingWebhookConfiguration ingress-nginx-admission

https://blog.lepape.me/local-kubernetes-cluster-with-ingress/

UHULLLLLLLLLLLLL
kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80

http://foo.127.0.0.1.nip.io:8080/
http://bar.127.0.0.1.nip.io:8080/

https://github.com/kubernetes/ingress-nginx/issues/13002
