#!/bin/bash

set -e

CLUSTER_NAME=pikakube

kind delete cluster -n $CLUSTER_NAME

echo "Cluster $CLUSTER_NAME deleted!"
