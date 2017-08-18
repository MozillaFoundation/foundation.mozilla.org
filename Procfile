release: ls network-api/app/networkapi && python network-api/app/manage.py migrate
web: cd network-api/app && gunicorn networkapi.wsgi:application
