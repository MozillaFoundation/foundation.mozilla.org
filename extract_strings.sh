#!/usr/bin/env bash

cd network-api

python manage.py makemessages -l de -l es -l fr -l pl -l pt_BR --keep-pot --no-wrap --ignore=networkapi/wagtailcustomization/* --ignore=networkapi/wagtail_l10n_customization/* --ignore=networkapi/settings.py --ignore=networkapi/wagtailpages/__init__.py

mv ./locale/django.pot ./locale/templates/LC_MESSAGES/django.pot
