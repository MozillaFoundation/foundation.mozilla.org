#!/usr/bin/env python
# import os
# import sys

import requests

# TODO: replace by os.environ.get("TRAVIS_PULL_REQUEST")
PR_NUMBER = "3730"
# TODO: encrypt github_token for travis
# GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")


def get_tags():
    pr_url = f"https://api.github.com/repos/mozilla/foundation.mozilla.org/pulls/{PR_NUMBER}"

    r = requests.get(pr_url).raise_for_status()
    print(r.json())


def check_tags():
    pass


if __name__ == "__main__":
    get_tags()
