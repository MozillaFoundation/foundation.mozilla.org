release: cd network-api && python ./manage.py migrate --no-input && python ./manage.py block_inventory && python ./manage.py sync_page_translation_fields && python ./manage.py update_translation_fields && python ./manage.py clear_cache
web: cd network-api && gunicorn networkapi.wsgi:application
