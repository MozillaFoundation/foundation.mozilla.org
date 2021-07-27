#!/usr/bin/env bash

cd network-api

# Django Migrations
python ./manage.py migrate --no-input

# Wagtail block inventory
python ./manage.py block_inventory

# Wagtail translations
# TODO: May need to add in auto syncing using wagtail-localize in the future.

# Clear cache for BuyersGuide
python ./manage.py clear_cache
