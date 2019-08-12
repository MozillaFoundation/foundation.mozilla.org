#!/usr/bin/env bash

cd network-api

# Django Migrations
python ./manage.py migrate --no-input

# Wagtail block inventory
python ./manage.py block_inventory

# Wagtail translations
python ./manage.py sync_page_translation_fields
python ./manage.py update_translation_fields

# Get the latest Portuguese (Brazil) translation file from Pontoon
cp ./locale/pt_BR/LC_MESSAGES/django.po ./locale/pt/LC_MESSAGES/django.po

# Compile the Django template translations
python ./manage.py compilemessages

# Clear cache for BuyersGuide
python ./manage.py clear_cache
