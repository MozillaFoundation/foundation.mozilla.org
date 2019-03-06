#!/usr/bin/env python
import json
import os
from urllib import request
from urllib.error import HTTPError

PR_NUMBER = os.environ.get("TRAVIS_PULL_REQUEST")
# TODO: encrypt github_token for travis
# GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
# TODO: select labels + create them on Github if necessary
CI_LABELS = ["Frontend", "Backend", "Python", "Javascript"]


def get_labels():
    pr_url = "https://api.github.com/repos/mozilla/foundation.mozilla.org/pulls/{}".format(PR_NUMBER)

    try:
        with request.urlopen(pr_url) as f:
            json_response = json.load(f)
    except HTTPError as error:
        print(error)
        return []
    try:
        labels = json_response["labels"]
        return [label["name"] for label in labels]
    except KeyError:
        print("No label found, running all tests")
        return []


def check_labels(labels_list):
    travis_labels = []
    [travis_labels.append(label) for label in labels_list if label in CI_LABELS]

    print(",".join(travis_labels))


if __name__ == "__main__":
    all_labels = get_labels()
    if all_labels:
        check_labels(all_labels)
