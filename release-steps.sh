#!/usr/bin/env bash
set -eo pipefail

# Django Migrations
MIGRATE_FLAGS="--no-input"

# For review apps. See if SKIP_MIGRATION_CHECKS env variable is set.
# If so then add --skip-checks for more overhead.

if [[ "${SKIP_MIGRATION_CHECKS:-0}" == "1" ]]; then
  MIGRATE_FLAGS="$MIGRATE_FLAGS --skip-checks"
fi

python ./manage.py migrate $MIGRATE_FLAGS --verbosity 3
# Clear cache for BuyersGuide
python ./manage.py clear_cache