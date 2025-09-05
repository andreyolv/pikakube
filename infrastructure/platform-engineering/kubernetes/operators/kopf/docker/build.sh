#!/bin/bash

set -e

REPONAME=andrey
TAG=datagen-operator:latest

docker build -t $TAG .

docker tag $TAG andreyolv/$TAG
echo 'Image tagged'
docker push andreyolv/$TAG
