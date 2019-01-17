cd network-api

@REM Django Migrations
python ./manage.py migrate --no-input

@REM Wagtail block inventory
python ./manage.py block_inventory

@REM Wagtail translations
python ./manage.py sync_page_translation_fields
python ./manage.py update_translation_fields

@REM Clear cache for BuyersGuide
python ./manage.py clear_cache
