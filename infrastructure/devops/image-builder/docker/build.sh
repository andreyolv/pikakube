#!/bin/bash

set -e

REPONAME=andrey
TAG=flink-python-example:latest

docker build -t $TAG .

docker tag $TAG andreyolv/$TAG
echo 'Image tagged'
docker push andreyolv/$TAG
