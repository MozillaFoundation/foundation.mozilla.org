#!/usr/bin/env bash

if [ $TRAVIS_EVENT_TYPE == "pull_request" ]; then
  echo "Configuring for pull request testing.."
  export NODE_TAG=$TRAVIS_PULL_REQUEST_BRANCH-node;
  export PYTHON_TAG=$TRAVIS_PULL_REQUEST_BRANCH-python;
  export APP_BUILD_TAG=$TRAVIS_PULL_REQUEST_BRANCH-app-build;
  export CYPRESS_TAG=$TRAVIS_PULL_REQUEST_BRANCH-cypress;
else
  echo "Configuring for branch testing"
  export NODE_TAG=$TRAVIS_BRANCH-node;
  export PYTHON_TAG=$TRAVIS_BRANCH-python;
  export APP_BUILD_TAG=$TRAVIS_BRANCH-app-build;
  export CYPRESS_TAG=$TRAVIS_BRANCH-cypress;
fi

echo "\$NODE_TAG: $NODE_TAG"
echo "\$PYTHON_TAG: $PYTHON_TAG"
echo "\$APP_BUILD_TAG: $APP_BUILD_TAG"
