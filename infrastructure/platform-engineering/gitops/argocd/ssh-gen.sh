#!/bin/bash

set -e

GITREPOSITORY=youer_repo
ENV=prd

# Generate ssh-keygen
mkdir $GITREPOSITORY
yes "" | ssh-keygen -f $GITREPOSITORY/id_rsa -N ""

echo "SSH Key Created!"

echo "Add public key into your repository in https://github.com/org/$GITREPOSITORY/settings/keys"
echo "Recommended github deploy name: argocd-ssh-$ENV-$GITREPOSITORY"
echo "Public Key bellow:"
cat $GITREPOSITORY/id_rsa.pub

# k port-forward svc/argocd-server -n argocd 8080:443
# argocd login localhost:8080 --username admin --password xxxxxxxxxxxxxxx --insecure
# argocd repo add git@github.com:org/repo.git --ssh-private-key-path youer_repo/id_rsa
