#!/bin/bash

set -e

# Update devbox version
devbox version update

# Update packages in your devbox.json
devbox update
