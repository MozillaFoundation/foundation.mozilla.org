release: cd network-api && python app/manage.py --no-input migrate && python app/manage.py heroku_release
web: cd network-api/app && gunicorn networkapi.wsgi:application
