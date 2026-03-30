#!/usr/bin/env bash
set -euo pipefail

restore_schema_snapshot() {
  echo "Restoring schema from snapshot."

  local s3_uri
  s3_uri="s3://${AWS_REVIEW_APP_SNAPSHOT_BUCKET}/${AWS_REVIEW_APP_SNAPSHOT_PATH}"

  echo "Generating presigned URL for schema snapshot: ${s3_uri}"

  SNAPSHOT_URL="$(
    AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID_REVIEW_APP_SNAPSHOT}" \
    AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY_REVIEW_APP_SNAPSHOT}" \
    AWS_DEFAULT_REGION="${AWS_REVIEW_APP_SNAPSHOT_REGION}" \
    aws s3 presign "${s3_uri}" --expires-in "300"
  )"

  echo "Downloading schema snapshot..."
  curl -fSL "$SNAPSHOT_URL" -o /tmp/schema.sql || { echo "ERROR: Failed to download schema from: '$SNAPSHOT_URL'"; exit 1; }

  echo "Applying schema to DATABASE_URL..."
  psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f /tmp/schema.sql

  echo "Schema restore complete."
}

if [ "${INIT_DB_FROM_SNAPSHOT:-}" = "True" ]; then
  restore_schema_snapshot
else
  echo "No snapshot mode set. Skipping DB restore, continuing to migrate."
fi

# Django Migrations
python ./manage.py migrate --no-input

# Clear cache for BuyersGuide
python ./manage.py clear_cache