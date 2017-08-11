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
    if not settings.HEROKU_APP_BUILD_URL:
        return logger.warn('settings.HEROKU_APP_BUILD_URL '
                           'must be set to trigger builds')

    if not settings.GITHUB_PROJECT_MASTER_TAR_URL:
        return logger.warn('settings.GITHUB_PROJECT_MASTER_TAR_URL '
                           'must be set to trigger builds')

    if not settings.HEROKU_API_TOKEN:
        return logger.warn('settings.HEROKU_API_TOKEN '
                           'must be set to trigger builds')

    data = {
        'source_blob': {
            'url': settings.GITHUB_PROJECT_MASTER_TAR_URL
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.heroku+json; version=3',
        'Authorization': 'Bearer {}'.format(settings.HEROKU_API_TOKEN)
    }

    build_request = requests.post(
        settings.HEROKU_APP_BUILD_URL,
        json=data,
        headers=headers
    )

    if build_request.status_code != 201:
        return logger.error('The Build was not started: {}'.format(build_request.text))  # noqa

    try:
        responseJSON = build_request.json()
        logger.info('Build started. output stream at: {}'.format(
            responseJSON.output_stream_url
        ))
    except Exception as e:
        logger.error('Error parsing response JSON from Heroku: {}'.format(e))
