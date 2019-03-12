#!/usr/bin/env sh

set -x # echo commands before running them

pip install --upgrade pip
pip install pipenv
pipenv install --dev --deploy
