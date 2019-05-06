#!/usr/bin/env bash

# Load environment vars
. ./travis/scripts/environment.sh

# Run CSS/JS linters
docker run -it $DOCKER_REPO:$NODE_TAG npm run test
