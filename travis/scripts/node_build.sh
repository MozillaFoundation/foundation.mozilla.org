#!/usr/bin/env bash

# Load environment vars
. .travis/scripts/environment.sh

# Pull the latest wagtail docker image from our Docker Hub repo
docker pull $DOCKER_REPO:$NODE_TAG || true

# Build an updated image, using cache
docker build --pull \
  --cache-from $DOCKER_REPO:$NODE_TAG \
  --tag $DOCKER_REPO:$NODE_TAG \
  --file "./travis/Dockerfile.node" .

# Authenticate with Docker Hub
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

# Push the latest build to Docker Hub
docker push $DOCKER_REPO:$NODE_TAG
