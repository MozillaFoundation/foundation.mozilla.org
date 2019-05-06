#!/usr/bin/env bash

if [ $TRAVIS_EVENT_TYPE == "pull_request" ]; then
  export NODE_TAG=$TRAVIS_PULL_REQUEST_BRANCH-node;
  export PYTHON_TAG=$TRAVIS_PULL_REQUEST_BRANCH-python;
  export APP_BUILD_TAG=$TRAVIS_PULL_REQUEST_BRANCH-app-build;
  export CYPRESS_TAG=$TRAVIS_PULL_REQUEST_BRANCH-cypress;
else
  export NODE_TAG=$TRAVIS_BRANCH-node;
  export PYTHON_TAG=$TRAVIS_BRANCH-python;
  export APP_BUILD_TAG=$TRAVIS_BRANCH-app-build;
  export CYPRESS_TAG=$TRAVIS_BRANCH-cypress;
fi

export PYTHON_TAG=$PYTHON_TAG
export APP_BUILD_TAG=$APP_BUILD_TAG
export CYPRESS_TAG=$CYPRESS_TAG
