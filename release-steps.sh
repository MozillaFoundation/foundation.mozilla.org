#!/usr/bin/env bash
set -eo pipefail

cd network-api

# Django Migrations
python ./manage.py migrate --no-input

# Temporary Step 2 for migrating to custom image model: data migration for images
python ./manage.py migrate_legacy_images

# Clear cache for BuyersGuide
python ./manage.py clear_cache
