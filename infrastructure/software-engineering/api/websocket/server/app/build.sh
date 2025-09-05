#!/bin/bash

set -e

REPONAME=andreyolv
TAG=websockets:1.1

docker build -t $TAG .

docker tag $TAG $REPONAME/$TAG
echo 'Image tagged'

kind load docker-image $REPONAME/$TAG --name pikakube
echo 'Image uploaded to local kind'
