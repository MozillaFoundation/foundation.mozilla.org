#!/usr/bin/env sh

set -x # echo commands before running them

pip install --upgrade pip
pip install -r requirements.txt -r dev-requirements.txt
