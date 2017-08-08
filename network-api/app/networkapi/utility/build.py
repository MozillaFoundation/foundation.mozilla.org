import requests
import logging

from mezzanine.conf import settings
from networkapi.utility.decorators import debounce_and_throttle

logger = logging.getLogger(__name__)


@debounce_and_throttle(
    settings.BUILD_DEBOUNCE_SECONDS,
    settings.BUILD_THROTTLE_SECONDS
)
def build_static_site(sender, instance, **kwargs):
    if not settings.BUILD_TRIGGER_URL:
        return logger.warn('settings.BUILD_TRIGGER_URL '
                           'must be set to trigger builds')

    build_request = requests.post(settings.BUILD_TRIGGER_URL)

    if build_request.status_code != 201:
        logger.error('The Build was not started: {}'.format(build_request.text))  # noqa
