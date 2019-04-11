FROM node:8-alpine

WORKDIR /app/

# Copy package files in the container
COPY package.json package-lock.json ./

RUN apk add --no-cache \
    zlib-dev \
    build-base

RUN npm install

# Install visual testing tools separately with CI true to suppress the hundreds lines of "unziping".
# Might replace it by a silent flag if this PR gets merged: https://github.com/cypress-io/cypress/pull/2706
RUN CI=true npm run cypress:install
