#!/bin/bash

set -e

REPONAME=andrey
TAG=hive-azure:latest

docker build -t $TAG .

docker tag $TAG andreyolv/$TAG
echo 'Image tagged'
docker push andreyolv/$TAG
