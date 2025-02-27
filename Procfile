release: ./release-steps.sh
web: cd foundation_cms && gunicorn legacy_cms.wsgi:application --preload --max-requests 2000
