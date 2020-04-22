release: ./release-steps.sh
web: cd network-api && gunicorn networkapi.wsgi:application --preload --max-requests 2000
