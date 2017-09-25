release: cd network-api && python network-api/app/manage.py --no-input migrate && python networkapi/app/manage.py heroku_release
web: cd network-api/app && gunicorn networkapi.wsgi:application
