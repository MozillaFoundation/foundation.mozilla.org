#!/usr/bin/env bash
set -euo pipefail

restore_schema_snapshot() {
  echo "Restoring schema from snapshot."

  TABLE_EXISTS=$(psql "$DATABASE_URL" -tAc "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'auth_group')")

  if [ "$TABLE_EXISTS" = "t" ]; then
    echo "Database already initialized, skipping restore."
  else

    local s3_uri
    s3_uri="s3://${AWS_REVIEW_APP_SNAPSHOT_BUCKET}/${AWS_REVIEW_APP_SNAPSHOT_PATH}"

    echo "Generating presigned URL for schema snapshot: ${s3_uri}"

    SNAPSHOT_URL="$(
      AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID_REVIEW_APP_SNAPSHOT}" \
      AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY_REVIEW_APP_SNAPSHOT}" \
      AWS_DEFAULT_REGION="${AWS_REVIEW_APP_SNAPSHOT_REGION}" \
      aws s3 presign "${s3_uri}" --expires-in "300"
    )"


      echo "Generating presigned URL for schema snapshot: $S3_SNAPSHOT_PATH"
      SNAPSHOT_URL=$(aws s3 presign "$S3_SNAPSHOT_PATH")

      echo "Downloading snapshot..."
      curl -fSL "$SNAPSHOT_URL" -o /tmp/snapshot.dump || { echo "ERROR: Failed to download from '$SNAPSHOT_URL'"; exit 1; }

      echo "Restoring database..."
      pg_restore --no-owner --no-acl -d "$DATABASE_URL" /tmp/snapshot.dump
      echo "Restore complete."
  fi

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