#!/usr/bin/env bash

echo -e "\033[92mRunning Python linter\033[0m"
pipenv run flake8 tasks.py network-api/

echo -e "\033[92mRunning Python tests\033[0m"
pipenv run coverage run --source './network-api/networkapi' network-api/manage.py test networkapi
