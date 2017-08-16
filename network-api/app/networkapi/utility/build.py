import requests
import logging

from mezzanine.conf import settings
from networkapi.utility.decorators import debounce_and_throttle

logger = logging.getLogger(__name__)


def getJSON(req):
    try:
        return req.json()
    except Exception:
        return None


@debounce_and_throttle(
    settings.BUILD_DEBOUNCE_SECONDS,
    settings.BUILD_THROTTLE_SECONDS
)
def build_static_site(sender, instance, **kwargs):
    if not settings.HEROKU_APP_NAME:
        return logger.warn('settings.HEROKU_APP_NAME '
                           'must be set to trigger builds')

    if not settings.GITHUB_PROJECT_MASTER_TAR_URL:
        return logger.warn('settings.GITHUB_PROJECT_MASTER_TAR_URL '
                           'must be set to trigger builds')

    if not settings.HEROKU_API_TOKEN:
        return logger.warn('settings.HEROKU_API_TOKEN '
                           'must be set to trigger builds')

    build_url = 'https://api.heroku.com/apps/{}/builds'.format(
        settings.HEROKU_APP_NAME
    )

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.heroku+json; version=3',
        'Authorization': 'Bearer {}'.format(settings.HEROKU_API_TOKEN)
    }

    build_payload = {
        'source_blob': {
            'url': settings.GITHUB_PROJECT_MASTER_TAR_URL
        }
    }

    # get a list of builds for the app
    list_builds = requests.get(build_url, headers=headers)

    if list_builds.status_code != 200:
        return logger.error('Could not list builds: {}'.format(list_builds.text))  # noqa

    responseJSON = getJSON(list_builds)

    if not responseJSON:
        return logger.error('did not receive valid JSON from the Heroku build and release API')  # noqa

    # return early if there's already a build in process for this app
    if responseJSON[0].status == 'pending':
        return logger.info('A Build is already in progress')

    build_request = requests.post(
        build_url,
        json=build_payload,
        headers=headers
    )

    if build_request.status_code != 201:
        return logger.error('The Build was not started: {}'.format(build_request.text))  # noqa

    responseJSON = getJSON(build_request)

    if not responseJSON:
        return logger.error('Error parsing response JSON from Heroku')

    logger.info('Build started. output stream at: {}'.format(
        responseJSON['output_stream_url']
    ))
