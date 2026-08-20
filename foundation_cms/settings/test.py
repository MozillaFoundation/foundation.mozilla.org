# Wildcard import so this module has every setting from base.py, plus the one
# override below. flake8 can't tell whether wildcard-imported names get used,
# so it would otherwise warn here (F403) -- suppressed intentionally.
from .base import *  # noqa: F403

# Skip the manifest-based static storage in tests so the backend test suite
# doesn't need `collectstatic` to have run first.
STORAGES["staticfiles"] = {  # noqa: F405
    "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
}
