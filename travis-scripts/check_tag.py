#!/usr/bin/env python

import os

test = os.environ.get("TRAVIS_PULL_REQUEST")
print(test)
