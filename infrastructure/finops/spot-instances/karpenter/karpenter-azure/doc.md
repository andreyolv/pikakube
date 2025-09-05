https://github.com/Azure/karpenter-provider-azure

https://github.com/Azure/karpenter-provider-azure/blob/main/hack/monitoring/grafana-values.yaml

https://github.com/Azure/karpenter-provider-azure/issues/696#issuecomment-2703637386
https://github.com/Azure/karpenter-provider-azure/issues/683

export CLUSTER_NAME=xxxxxx
export RG=xxxxxxxxx
export LOCATION=eastus2
export KARPENTER_NAMESPACE=kube-system

export KARPENTER_VERSION=1.5.4
curl -sO https://raw.githubusercontent.com/Azure/karpenter-provider-azure/v${KARPENTER_VERSION}/karpenter-values-template.yaml
curl -sO https://raw.githubusercontent.com/Azure/karpenter-provider-azure/v${KARPENTER_VERSION}/hack/deploy/configure-values.sh
chmod +x ./configure-values.sh && ./configure-values.sh ${CLUSTER_NAME} ${RG} karpenter-sa karpentermsi-aks-prd

kubectl get secrets \
  --field-selector type=bootstrap.kubernetes.io/token \
  -o jsonpath='{range .items[*]}{.data.token-secret}{"\n"}{end}' \
  | while read encoded; do echo "$encoded" | base64 -d; echo; done

kubectl get secret karpenter-join-token \
  -o jsonpath="{.data.KUBELET_BOOTSTRAP_TOKEN}" | base64 -d

