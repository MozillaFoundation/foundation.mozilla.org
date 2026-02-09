#!/usr/bin/env bash
set -eo pipefail
# Idea borrowed from mofo-cron's prod to stage copy
update_site_bindings() {
  if [ -z "${HEROKU_APP_NAME:-}" ]; then
    echo "HEROKU_APP_NAME is not set. Cannot update site bindings."
    return 1
  fi

  RA_HOST="${HEROKU_APP_NAME}.mofostaging.net"
  LEGACY_RA_HOST="legacy-${HEROKU_APP_NAME}.mofostaging.net"
  MOZFEST_RA_HOST="mozfest-${HEROKU_APP_NAME}.mofostaging.net"

  echo "Updating site bindings for review app: $HEROKU_APP_NAME"

  echo "Updating django_site..."
  psql "$DATABASE_URL" -v ON_ERROR_STOP=1 <<SQL
UPDATE django_site
SET domain = '${RA_HOST}'
WHERE domain LIKE '%.mofostaging.net';
SQL

  echo "Updating wagtailcore_site..."
  psql "$DATABASE_URL" -v ON_ERROR_STOP=1 <<SQL
-- Update the three known sites by site_name, avoiding collisions
UPDATE wagtailcore_site
SET hostname = '${RA_HOST}', port = 80
WHERE site_name = 'Mozilla Foundation';

UPDATE wagtailcore_site
SET hostname = '${LEGACY_RA_HOST}', port = 80
WHERE site_name = 'Legacy Site';

UPDATE wagtailcore_site
SET hostname = '${MOZFEST_RA_HOST}', port = 80
WHERE site_name = 'Mozilla Festival';
SQL

  echo "Site bindings updated."
}

db_already_init() {
  # If wagtailcore_site exists and has at least 1 row, assume snapshot already applied
  psql "$DATABASE_URL" -tAc "SELECT 1 FROM wagtailcore_site LIMIT 1;" 2>/dev/null | grep -q 1
}

# Restore review app backup
# Only run if a review app snapshot URL is provided
if [ -n "${RA_SNAPSHOT_URL:-}" ]; then
  if db_already_init; then
    echo "Database already appears to be initialized and seeded. Skipping DB restore."
  else
    echo "RA_SNAPSHOT_URL set and DB not seeded. Restoring database."

    echo "Downloading snapshot..."
    curl -fSL "$RA_SNAPSHOT_URL" -o /tmp/review.dump

    echo "Restoring to DATABASE_URL..."
    # Use pg_restore for custom format dumps (-F c)
    pg_restore --verbose --clean --if-exists --no-comments --no-acl --no-owner -d "$DATABASE_URL" /tmp/review.dump

    echo "DB restore complete."
    echo "Updating site bindings..."
    update_site_bindings
    echo "Site bindings update complete."
else
  echo "REVIEW_DUMP_URL not set. Skipping DB restore."
fi

# Django Migrations
python ./manage.py migrate --no-input

# Clear cache for BuyersGuide
python ./manage.py clear_cache

