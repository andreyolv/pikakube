https://github.com/fluxcd/flux2
https://github.com/fluxcd/helm-controller

Install & Update https://fluxcd.io/flux/cmd/#install-using-bash
curl -s https://fluxcd.io/install.sh | sudo FLUX_VERSION=2.4.0 bash
flux --version

flux bootstrap github \
  --owner=andreyolv \
  --repository=big-data-platform-on-k8s \
  --branch=main \
  --path=./clusters/dev \
  --components-extra=image-reflector-controller,image-automation-controller \
  --read-write-key \
  --personal

Useful flux commands:
```sh 
flux get kustomizations -A | kubectl get kustomizations -A
flux get sources chart -A
flux get sources git -A
flux get sources oci -A
k get helmrepositories -A
flux get helmreleases -A | flux get hr -A | kubectl get hr -A
flux get all
k get kustomizations.kustomize.toolkit.fluxcd.io -n flux-system -w
flux reconcile hr <helmrelease> -n <namespace>
flux suspend hr
flux resume hr
flux get image all
flux get all
```

k port-forward svc/source-controller 8080:80 -n flux-system

https://github.com/fluxcd/flux2/discussions/1599
