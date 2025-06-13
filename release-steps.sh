#!/usr/bin/env bash
set -eo pipefail

# Temporary Step 1 for migrating to custom image model: migrate images app
python ./manage.py migrate images

# Temporary Step 2 for migrating to custom image model: data migration for images
python ./manage.py migrate_legacy_images

# Django Migrations
python ./manage.py migrate --no-input

# Clear cache for BuyersGuide
python ./manage.py clear_cache