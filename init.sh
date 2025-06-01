#!/bin/bash

set -e

GITHUB_USER=andreyolv
GITHUB_REPOSITORY=pikakube

echo "Creating a Kind cluster..."
kind create cluster --config clusters/kind-configs/core.yaml

echo "Cluster created!"
echo "Installing Flux..."
flux bootstrap github \
  --token-auth \
  --owner=$GITHUB_USER \
  --repository=$GITHUB_REPOSITORY \
  --branch=main \
  --path=clusters/dev \
  --components-extra=image-reflector-controller,image-automation-controller \
  --read-write-key=true

echo "Flux installed!"