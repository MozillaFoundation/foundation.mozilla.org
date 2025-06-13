#!/usr/bin/env bash
set -eo pipefail

# Django Migrations
python ./manage.py migrate --no-input

# Clear cache for BuyersGuide
python ./manage.py clear_cache