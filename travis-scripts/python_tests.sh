#!/usr/bin/env bash

echo -e "Running Python linter"
pipenv run flake8 tasks.py network-api/ --count

echo -e "Running Python tests"
pipenv run coverage run --source './network-api/networkapi' network-api/manage.py test networkapi
