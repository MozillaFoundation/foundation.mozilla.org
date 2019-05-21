#!/usr/bin/env bash

if [ $TRAVIS_EVENT_TYPE == "pull_request" ]; then
  echo "Configuring for pull request testing.."
  export NODE_TAG=$TRAVIS_PULL_REQUEST_BRANCH-node;
  export WAGTAIL_APP_TAG=$TRAVIS_PULL_REQUEST_BRANCH-wagtail-app;
  export APP_BUILD_TAG=$TRAVIS_PULL_REQUEST_BRANCH-app-build;
  export CYPRESS_TAG=$TRAVIS_PULL_REQUEST_BRANCH-cypress;
else
  echo "Configuring for branch testing"
  export NODE_TAG=$TRAVIS_BRANCH-node;
  export WAGTAIL_APP_TAG=$TRAVIS_BRANCH-wagtail-app;
  export APP_BUILD_TAG=$TRAVIS_BRANCH-app-build;
  export CYPRESS_TAG=$TRAVIS_BRANCH-cypress;
fi

echo "\$NODE_TAG: $NODE_TAG"
echo "\$WAGTAIL_APP_TAG: $WAGTAIL_APP_TAG"
echo "\$APP_BUILD_TAG: $APP_BUILD_TAG"
