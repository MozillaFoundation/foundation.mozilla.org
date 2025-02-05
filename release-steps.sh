#!/usr/bin/env bash
set -eo pipefail

cd network-api

# Django Migrations
python ./manage.py migrate --fake-initial --no-input

# Clear cache for BuyersGuide
python ./manage.py clear_cache
