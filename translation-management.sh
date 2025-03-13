#!/usr/bin/env bash

set -euo pipefail

# Pretty printing functions
NORMAL=$(tput sgr0)
GREEN=$(tput setaf 2; tput bold)
YELLOW=$(tput setaf 3)
RED=$(tput setaf 1)

function echored() {
  echo -e "$RED$*$NORMAL"
}

function echogreen() {
  echo -e "$GREEN$*$NORMAL"
}

function echoyellow() {
  echo -e "$YELLOW$*$NORMAL"
}

if [ $# -lt 1 ]
then
  echored "ERROR: not enough arguments supplied."
  echo "Usage: translation-management.sh *action*"
  echo "  - action: import, export"
  exit 1
fi

command="$1"

# Read path to local string repository from .env file
L10N_REPO=$(grep LOCAL_PATH_TO_L10N_REPO .env | cut -d '=' -f2)
L10N_REPO+="foundation/translations/"
CODE_REPO="./"

FOLDERS=(
  "foundation_cms/locale/"
  "foundation_cms/legacy_apps/templates/pages/buyersguide/about/locale/"
  "foundation_cms/legacy_apps/wagtailpages/templates/wagtailpages/pages/locale/"
  "foundation_cms/legacy_apps/wagtailpages/templates/wagtailpages/pages/youtube-regrets-2021/locale/"
  "foundation_cms/legacy_apps/wagtailpages/templates/wagtailpages/pages/youtube-regrets-2022/locale/"
  "foundation_cms/legacy_apps/mozfest/locale/"
)

# Array of locale codes in ab-CD format that need to be converted into ab_CD for Django
LOCALES=(
  "fy-NL"
  "pt-BR"
)

case $command in
  "import")
    echogreen "Importing latest translation files from fomo-l10n repository"
    for FOLDER in "${FOLDERS[@]}"; do
      cp -r "${L10N_REPO}${FOLDER}" "${CODE_REPO}${FOLDER}"

      # Django >=3.2 stopped processing locale codes containing hyphens, we need to move the files between the two folders
      for HYPHEN_LOCALE in "${LOCALES[@]}"; do
        cp -r "${L10N_REPO}${FOLDER}${HYPHEN_LOCALE}/" "${CODE_REPO}${FOLDER}${HYPHEN_LOCALE//-/_}/"
      done
    done
esac

case $command in
  "export")
    echogreen "Exporting generated translation files to fomo-l10n repository"
    for FOLDER in "${FOLDERS[@]}"; do
      cp -r "${CODE_REPO}${FOLDER}" "${L10N_REPO}${FOLDER}"

      # Django >=3.2 stopped processing locale codes containing hyphens, we need to move the files between the two folders
      for HYPHEN_LOCALE in "${LOCALES[@]}"; do
        cp -r "${CODE_REPO}${FOLDER}${HYPHEN_LOCALE//-/_}/" "${L10N_REPO}${FOLDER}${HYPHEN_LOCALE}/"
      done
    done
esac
