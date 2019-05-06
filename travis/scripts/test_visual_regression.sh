#!/usr/bin/env bash

# Load environment vars
. .travis/scripts/environment.sh

# Pull down the prebuilt cypress image
docker-compose -f travis/docker-compose.travis.yml pull cypress || true

# Update the cypress image if necessary
docker-compose -f travis/docker-compose.travis.yml build cypress

# Generate static assets for Django/Wagtail
docker-compose -f travis/docker-compose.travis.yml \
  run --rm \
  wagtail_cypress \
  python network-api/manage.py collectstatic --no-input --verbosity 0

# Prepare the database
docker-compose -f travis/docker-compose.travis.yml \
  run --rm \
  wagtail_cypress python network-api/manage.py migrate --no-input

# Update the block inventory
docker-compose -f travis/docker-compose.travis.yml \
  run --rm \
  wagtail_cypress python network-api/manage.py block_inventory

# update localisation data
docker-compose -f travis/docker-compose.travis.yml \
  run --rm \
  wagtail_cypress python network-api/manage.py sync_page_translation_fields

docker-compose -f travis/docker-compose.travis.yml \
  run --rm \
  wagtail_cypress python network-api/manage.py update_translation_fields

# Populate the database with test data
docker-compose -f travis/docker-compose.travis.yml \
  run --rm \
  wagtail_cypress python network-api/manage.py load_fake_data

# Run the visual regression tests on the test site
docker-compose -f travis/docker-compose.travis.yml up cypress

# Authenticate with Docker Hub
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

# Push the cypress image up to Docker Hub
docker-compose -f travis/docker-compose.travis.yml push cypress
