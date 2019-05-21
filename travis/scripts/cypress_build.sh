#!/usr/bin/env bash

# Expand aliases (disabled by default in non-interactive shells)
shopt -s expand_aliases

# Load environment vars
. ./travis/scripts/environment.sh

# Alias docker-compose command
alias dc="docker-compose -f travis/docker-compose.travis.yml"

# Pull down the prebuilt cypress image
dc pull cypress || true

# Update the cypress image if necessary
dc build cypress

# Authenticate with Docker Hub
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

# Push the cypress image up to Docker Hub
dc push cypress
