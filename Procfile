release: ./release-steps.sh
web: cd network-api && gunicorn legacy_cms.wsgi:application --preload --max-requests 2000
