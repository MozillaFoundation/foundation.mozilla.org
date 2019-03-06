#!/usr/bin/env python
import os

import requests

# TODO remove: PR number = 2730
PR_NUMBER = os.environ.get("TRAVIS_PULL_REQUEST")
# TODO: encrypt github_token for travis
# GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
# TODO: select labels + create them on Github if necessary
CI_LABELS = ["Frontend", "Backend", "Python", "Javascript"]


def get_labels():
    pr_url = "https://api.github.com/repos/mozilla/foundation.mozilla.org/pulls/{}".format(PR_NUMBER)

    r = requests.get(pr_url)

    # TODO: do not fail and return an empty list + print error message + status
    r.raise_for_status()

    try:
        labels = r.json()["labels"]
        label_names = []
        [label_names.append(label["name"]) for label in labels]
    except KeyError:
        label_names = []
        print("No label found, running all tests")

    return label_names


def check_labels(labels_list):
    travis_labels = []
    [travis_labels.append(label) for label in labels_list if label in CI_LABELS]

    print(",".join(travis_labels))


if __name__ == "__main__":
    all_labels = get_labels()
    check_labels(all_labels)
