release: cd network-api && python ./manage.py migrate --no-input
web: cd network-api && gunicorn networkapi.wsgi:application
clock: python clock.py
