#!/usr/bin/env bash
set -euo pipefail

update_site_bindings() {
  # Idea borrowed from mofo-cron's prod to stage copy

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


restore_review_app_backup_if_needed() {

  if db_already_init; then
    echo "Database already appears to be initialized and seeded. Skipping DB restore."
    return 0
  fi

  echo "DB not initialized. Restoring database."


  local s3_uri
  s3_uri="s3://${AWS_REVIEW_APP_SNAPSHOT_BUCKET}/${AWS_REVIEW_APP_SNAPSHOT_PATH}"

  echo "Generating presigned URL for snapshot: ${s3_uri}"

  # Generate presigned URL using the snapshot-specific credentials, scoped to this command only
  SNAPSHOT_URL="$(
    AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID_REVIEW_APP_SNAPSHOT}" \
    AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY_REVIEW_APP_SNAPSHOT}" \
    AWS_DEFAULT_REGION="${AWS_REVIEW_APP_SNAPSHOT_REGION}" \
    aws s3 presign "${s3_uri}" --expires-in "300"
  )"

  echo "Downloading snapshot..."
  curl -fSL "$SNAPSHOT_URL" -o /tmp/review.dump

  echo "Restoring to DATABASE_URL..."
  pg_restore --verbose --clean --if-exists --no-comments --no-acl --no-owner -d "$DATABASE_URL" /tmp/review.dump

  echo "DB restore complete."
  echo "Updating site bindings..."
  update_site_bindings
  echo "Site bindings update complete."
}

# Restore DB (if needed) before migrations
restore_review_app_backup_if_needed

# Django Migrations
python ./manage.py migrate --no-input

# Clear cache for BuyersGuide
python ./manage.py clear_cache