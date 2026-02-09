#!/usr/bin/env bash
set -eo pipefail

# Django Migrations
#python ./manage.py migrate --no-input

# Restore review app backup
set -euo pipefail

# Only run if a review app snapshot URL is provided
if [ -z "${RA_SNAPSHOT_URL:-}" ]; then
    echo "No RA_SNAPSHOT_URL set. Skipping DB restore."
    echo "Downloading dump..."
    curl -fSL "$RA_SNAPSHOT_URL" -o /tmp/review.dump

    echo "Restoring to DATABASE_URL..."
    # Use pg_restore for custom format dumps (-F c)
    pg_restore --verbose --clean --no-acl --no-owner -d "$DATABASE_URL" /tmp/review.dump

    echo "DB restore complete."
fi

python ./manage.py migrate --no-input

# Clear cache for BuyersGuide
python ./manage.py clear_cache