@REM Django Migrations
pipenv run python network-api\manage.py migrate --no-input

@REM Wagtail block inventory
pipenv run python network-api\manage.py block_inventory

@REM Wagtail translations
pipenv run python network-api\manage.py sync_page_translation_fields
pipenv run python network-api\manage.py update_translation_fields

@REM Clear cache for BuyersGuide
pipenv run python network-api\manage.py clear_cache
