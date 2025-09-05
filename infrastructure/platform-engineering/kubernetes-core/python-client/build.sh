#!/bin/bash

set -e

REPONAME=andrey
TAG=kubernetes-client:latest

docker image build . -t $TAG

docker tag $TAG andreyolv/$TAG
echo 'Image tagged'
docker push andreyolv/$TAG
