release: ./release-steps.sh
web: gunicorn foundation_cms.wsgi:application --preload --max-requests 2000 --max-requests-jitter 400
