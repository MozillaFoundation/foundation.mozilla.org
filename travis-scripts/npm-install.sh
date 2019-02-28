#!/usr/bin/env sh

set -x # echo commands before running them

npm install -g npm@latest # Needed to use npm ci
npm ci # Use package-lock.json
