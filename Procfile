release: cd network-api && python app/manage.py migrate --no-input && python app/manage.py heroku_release
web: cd network-api/app && gunicorn networkapi.wsgi:application
