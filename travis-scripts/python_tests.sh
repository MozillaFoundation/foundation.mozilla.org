#!/usr/bin/env bash

echo "Running linter"
pipenv run flake8 tasks.py network-api/

echo "Running tests"
pipenv run coverage run --source './network-api/networkapi' network-api/manage.py test networkapi
