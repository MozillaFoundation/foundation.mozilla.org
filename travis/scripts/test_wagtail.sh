#!/usr/bin/env bash

# Load environment vars
. ./travis/scripts/environment.sh

# Run flake8 inside the wagtail container
docker-compose -f travis/docker-compose.travis.yml \
  run --rm \
  wagtail \
  flake8 tasks.py network-api

# Run the Django/Wagtail tests and report code coverage to coveralls
docker-compose -f travis/docker-compose.travis.yml \
  run --rm \
  -e COVERALLS_REPO_TOKEN=$COVERALLS_REPO_TOKEN \
  -e TRAVIS_JOB_ID=$TRAVIS_JOB_ID \
  wagtail \
  sh -c "coverage run --source './network-api/networkapi' network-api/manage.py test networkapi && coveralls"
