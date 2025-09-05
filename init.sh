#!/bin/bash

set -e

GITHUB_USER=andreyolv
GITHUB_REPOSITORY=pikakube

echo "Creating a Kind cluster..."
kind create cluster --config clusters/kind-configs/core.yaml
echo "Cluster created!"

echo "Installing helm flux-operator..."
helm install flux-operator oci://ghcr.io/controlplaneio-fluxcd/charts/flux-operator --namespace flux-system --create-namespace
echo "Flux-operator installed!"

flux create secret githubapp flux-system \
  --app-id=$PIKAKUBE_FLUX_OPERATOR_APP_ID \
  --app-installation-id=$PIKAKUBE_FLUX_OPERATOR_INSTALLATION_ID \
  --app-private-key=infrastructure/platform-engineering/gitops/flux/flux-operator/pikakube-flux-operator.private-key.pem

kubectl apply -f infrastructure/platform-engineering/gitops/flux/flux-operator/fluxinstance.yaml

echo "Flux installed!"

kubectl create ns vault
kubectl apply -f infrastructure/security/secrets/vault/vault-dev/configmap-real.yaml
kubectl create ns ingress-nginx
kubectl apply -f infrastructure/security/certificates/mkcert/mkcert-tls-secret.yaml

echo "Basics manifests installed!"

kubens flux-system

kubectl wait fluxinstance flux --for=condition=Ready --timeout=5m

kubectl wait kustomization flux-system --for=condition=Ready --timeout=5m

kubectl wait kustomization nginx --for=condition=Ready --timeout=5m

kubectl wait kustomization kyverno --for=condition=Ready --timeout=5m

kubectl wait kustomization pikakube --for=condition=Ready --timeout=5m

kubectl wait kustomization vault --for=condition=Ready --timeout=5m

kubectl wait kustomization external-secrets --for=condition=Ready --timeout=5m

kubectl wait kustomization prometheus --for=condition=Ready --timeout=5m

kubectl wait kustomization grafana --for=condition=Ready --timeout=5m
