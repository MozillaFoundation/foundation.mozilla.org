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
CODE_REPO="foundation_cms/"

FOLDERS=(
  "legacy_apps/locale/"
  "legacy_apps/templates/pages/buyersguide/about/locale/"
  "legacy_apps/wagtailpages/templates/wagtailpages/pages/locale/"
  "legacy_apps/wagtailpages/templates/wagtailpages/pages/youtube-regrets-2021/locale/"
  "legacy_apps/wagtailpages/templates/wagtailpages/pages/youtube-regrets-2022/locale/"
  "legacy_apps/mozfest/locale/"
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
      # Step 1: Reset Django folder(s)
      echoyellow "  Removing existing folder: ${CODE_REPO}${FOLDER}"
      rm -rf "${CODE_REPO}${FOLDER}"

      # Step 2: Copy l10n (source of truth) to Django
      echoyellow "  Copying l10n folder: ${L10N_REPO}${FOLDER} into ${CODE_REPO}${FOLDER}"
      cp -r "${L10N_REPO}${FOLDER}" "${CODE_REPO}${FOLDER}"

      # Step 3: Remove stray underscore-locale dirs / symlinks (cleanup)
      for HYPHEN_LOCALE in "${LOCALES[@]}"; do
        UNDERSCORE="${CODE_REPO}${FOLDER}${HYPHEN_LOCALE//-/_}"
        if [[ -e "$UNDERSCORE" ]]; then
          echoyellow "  Removing stray underscore locale (usually symlinks): $UNDERSCORE"
          rm -rf "$UNDERSCORE"
        fi
      done

      # Step 4: Copy hyphenated → underscore for Django
      for HYPHEN_LOCALE in "${LOCALES[@]}"; do
        cp -r "${L10N_REPO}${FOLDER}${HYPHEN_LOCALE}/" "${CODE_REPO}${FOLDER}${HYPHEN_LOCALE//-/_}/"

        # Step 5: Remove hyphenated l10n dirs since not needed in Django repo (i.e. pt-BR)
        HYPHEN_LOCALE_PATH="${CODE_REPO}${FOLDER}${HYPHEN_LOCALE}"
        if [[ -e "$HYPHEN_LOCALE_PATH" ]]; then
          echoyellow "  Removing hyphen locale from code repo: $HYPHEN_LOCALE_PATH"
          rm -rf "$HYPHEN_LOCALE_PATH"
        fi

      done
    done
    ;;
esac

case $command in
  "export")
    echogreen "Exporting generated translation files to fomo-l10n repository"
    for FOLDER in "${FOLDERS[@]}"; do
      # Step 1: Reset l10n folder(s)
      echoyellow "  Removing existing folder: ${L10N_REPO}${FOLDER}"
      rm -rf "${L10N_REPO}${FOLDER}"

      # Step 2: Copy Django (new source of truth) to l10n
      echoyellow "  Copying Django folder: ${CODE_REPO}${FOLDER} into ${L10N_REPO}${FOLDER}"
      mkdir -p "${L10N_REPO}${FOLDER}"
      cp -r "${CODE_REPO}${FOLDER}"* "${L10N_REPO}${FOLDER}"

      # Step 3: Copy Django underscore dirs to l10n hyphen dirs for Pontoon (i.e. pt_BR in Django to pt-BR in l10n)
      for HYPHEN_LOCALE in "${LOCALES[@]}"; do
        cp -r "${CODE_REPO}${FOLDER}${HYPHEN_LOCALE//-/_}/" "${L10N_REPO}${FOLDER}${HYPHEN_LOCALE}/"

        # Step 4: Remove underscore locale dirs in l10n since not needed in l10n repo (i.e. pt_BR)
        UNDERSCORE_LOCALE_PATH="${L10N_REPO}${FOLDER}${HYPHEN_LOCALE//-/_}"
        if [[ -e "$UNDERSCORE_LOCALE_PATH" ]]; then
          echoyellow "  Removing underscore locale from l10n: $UNDERSCORE_LOCALE_PATH"
          rm -rf "$UNDERSCORE_LOCALE_PATH"
        fi
      
      done
    done
    ;;
esac