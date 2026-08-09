#!/bin/bash

set -e

REPOSITORY=andreyolv
TAG=pypi-server:0.0.1

docker build -t $TAG .

docker tag $TAG $REPOSITORY/$TAG
echo 'Image tagged'
docker push $REPOSITORY/$TAG
