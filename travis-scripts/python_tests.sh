#!/usr/bin/env bash

echo "Running Python linter"
pipenv run flake8 tasks.py network-api/

echo "Running Python tests"
pipenv run coverage run --source './network-api/networkapi' network-api/manage.py test networkapi
