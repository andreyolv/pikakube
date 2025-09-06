#!/bin/bash

set -e

REPONAME=andrey
TAG=prometheus-exporter:latest

docker build -t $TAG .

docker tag $TAG andreyolv/$TAG
echo 'Image tagged'
docker push andreyolv/$TAG
