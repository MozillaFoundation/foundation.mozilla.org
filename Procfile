release: cd network-api && python network-api/app/manage.py migrate && python networkapi/app/manage.py checkenv
web: cd network-api/app && gunicorn networkapi.wsgi:application
