#!/bin/bash
set -e

# This script can help automate migration conflicts and local environment
# It stashes your changes, pulls / checks out redesign branch makes a clean db, 
# rechecks out your branch / stash, detects any migrations that haven't run
# (and deletes them because these are probably just conflicting) and then regenerates them

YELLOW='\033[1;33m'
NC='\033[0m'

# Remember current branch
ORIGINAL_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Current branch: $ORIGINAL_BRANCH"

STASHED=false

# Stop current env if running
echo "Shutting down env..."
docker-compose down

# Check for uncommitted changes
if ! git diff-index --quiet HEAD -- || [ -n "$(git ls-files --others --exclude-standard)" ]; then
  echo
  echo -e "${YELLOW}You have uncommitted changes on this branch ($ORIGINAL_BRANCH).${NC}"
  echo "These changes will be temporarily stashed during this workflow."
  read -p "Do you want to continue with the stash workflow? [y/N]: " confirm
  if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Aborting."
    exit 1
  fi

  echo "Stashing changes (including untracked files)..."
  git stash --include-untracked || echo "Nothing to stash."
  STASHED=true
else
  echo "No uncommitted changes detected."
fi

# Checkout redesign branch and pull latest changes
echo "Checking out 'redesign' branch..."
git checkout redesign
echo "Pulling latest changes..."
git pull origin redesign

# Rebuild database from committed migrations
echo "Rebuilding DB from migrations..."
inv new-db

# Switch back to the original branch
echo "Switching back to $ORIGINAL_BRANCH..."
git checkout "$ORIGINAL_BRANCH"

# Reapply stashed changes if any
if $STASHED && git stash list | grep -q "WIP on $ORIGINAL_BRANCH"; then
  echo "Reapplying stashed changes..."
  git stash pop || echo "Nothing to pop or stash already applied."
fi

# Delete unapplied migration files
echo "Removing unapplied migration files..."
inv manage "showmigrations --plan" | grep '\[ \]' | awk '{print $3}' | tr -d '\r' | while read migration; do
  app=$(echo "$migration" | cut -d. -f1)
  mig=$(echo "$migration" | cut -d. -f2)
  file="foundation_cms/${app}/migrations/${mig}.py"
  echo "$file"
  if [ -f "$file" ]; then
    echo "  Deleting $file"
    rm "$file"
  fi
done

# Generate new migrations
echo "Generating fresh migrations..."
inv makemigrations

echo "Migration cleanup and regeneration complete. Feel free to migrate!"