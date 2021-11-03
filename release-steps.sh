#!/usr/bin/env bash

cd network-api

# Django Migrations
python ./manage.py migrate --no-input

# Clear cache for BuyersGuide
python ./manage.py clear_cache
