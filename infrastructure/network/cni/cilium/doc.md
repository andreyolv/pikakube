https://github.com/cilium/cilium
https://github.com/cilium/hubble
https://github.com/cilium/hubble-ui

https://artifacthub.io/packages/helm/cilium/cilium/
https://github.com/cilium/cilium/blob/master/install/kubernetes/cilium/values.yaml

install kind:
https://docs.cilium.io/en/stable/installation/kind/

kind load docker-image quay.io/cilium/cilium:v1.16.5 --name pikakube

cilium tem problemas com wsl, necessário atualizar versão do kernel do wsl
como ver qual versão do kernel
uname -r
5.15.153.1-microsoft-standard-WSL2

https://github.com/cilium/cilium/issues/17745#issuecomment-1004299480
https://dev.to/cslemes/usando-cilium-no-wsl-a1
https://medium.com/@nahelou.j/play-with-cilium-native-routing-in-kind-cluster-5a9e586a81ca
https://medium.com/@charled.breteche/kind-cluster-with-cilium-and-no-kube-proxy-c6f4d84b5a9d