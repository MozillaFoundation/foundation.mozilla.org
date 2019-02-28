#!/usr/bin/env sh

set -x # echo commands before running them

nvm install --lts=carbon
nvm use --lts=carbon
npm install -g npm@latest # Needed to use npm ci
npm ci # Use package-lock.json
