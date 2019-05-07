#!/usr/bin/env bash

# Load environment vars
. ./travis/scripts/environment.sh

# Alias docker-compose command
dc='docker-compose -f travis/docker-compose.travis.yml'

# Pull down the prebuilt cypress image
dc pull cypress || true

# Update the cypress image if necessary
dc build cypress

# Generate static assets for Django/Wagtail
dc run --rm wagtail_cypress \
  python network-api/manage.py collectstatic --no-input --verbosity 0

# Prepare the database
dc run --rm \
  wagtail_cypress python network-api/manage.py migrate --no-input

# Update the block inventory
dc run --rm \
  wagtail_cypress python network-api/manage.py block_inventory

# update localisation data
dc run --rm \
  wagtail_cypress python network-api/manage.py sync_page_translation_fields

dc run --rm \
  wagtail_cypress python network-api/manage.py update_translation_fields

# Populate the database with test data
dc run --rm \
  wagtail_cypress python network-api/manage.py load_fake_data

# Run the visual regression tests on the test site
dc up cypress

# Authenticate with Docker Hub
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

# Push the cypress image up to Docker Hub
dc push cypress
