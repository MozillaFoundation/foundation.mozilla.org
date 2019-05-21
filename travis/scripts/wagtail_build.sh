#!/usr/bin/env bash

# Load environment vars
. ./travis/scripts/environment.sh

# Pull the latest images from our Docker Hub repo
docker pull $DOCKER_REPO:$APP_BUILD_TAG || true
docker pull $DOCKER_REPO:$WAGTAIL_APP_TAG || true

# Build updated images, using cache
docker build --pull \
  --cache-from $DOCKER_REPO:$APP_BUILD_TAG \
  --tag $DOCKER_REPO:$APP_BUILD_TAG \
  --target node-build --file "./travis/Dockerfile.wagtail" .
docker build --pull \
  --cache-from $DOCKER_REPO:$APP_BUILD_TAG \
  --cache-from $DOCKER_REPO:$WAGTAIL_APP_TAG \
  --tag $DOCKER_REPO:$WAGTAIL_APP_TAG \
  --target application \
  --file "./travis/Dockerfile.wagtail" .

# Authenticate with Docker Hub
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

# Push images to Docker Hub
docker push $DOCKER_REPO:$APP_BUILD_TAG
docker push $DOCKER_REPO:$WAGTAIL_APP_TAG
