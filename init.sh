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