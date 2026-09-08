import logging

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = (2, 3)  # connect, read

API_URL = "https://boards-api.greenhouse.io/v1/boards/{token}/jobs"
EMBED_SCRIPT_URL = "https://boards.greenhouse.io/embed/job_board/js?for={token}"
HOSTED_BOARD_URL = "https://job-boards.greenhouse.io/{token}"

STATE_BOARD = "board"
STATE_EMPTY = "empty"
STATE_DEGRADED = "degraded"
STATE_UNAVAILABLE = "unavailable"

SUCCESS_STATES = (STATE_BOARD, STATE_EMPTY)


def _read_board_state(token):
    try:
        response = requests.get(API_URL.format(token=token), timeout=REQUEST_TIMEOUT)
    except requests.RequestException:
        logger.warning("Greenhouse job board request failed for token %r.", token, exc_info=True)
        return STATE_DEGRADED

    if response.status_code == 404:
        logger.error("Greenhouse has no job board for token %r.", token)
        return STATE_UNAVAILABLE

    if response.status_code != 200:
        logger.warning("Greenhouse job board returned HTTP %s for token %r.", response.status_code, token)
        return STATE_DEGRADED

    try:
        jobs = response.json()["jobs"]
    except (ValueError, TypeError, KeyError):
        jobs = None

    if not isinstance(jobs, list):
        logger.warning("Greenhouse job board returned an unexpected payload for token %r.", token)
        return STATE_DEGRADED

    return STATE_BOARD if jobs else STATE_EMPTY


def get_greenhouse_board_state(token):
    if not token:
        logger.warning("GREENHOUSE_BOARD_TOKEN is not set, so the job board cannot be rendered.")
        return STATE_UNAVAILABLE

    cache_key = f"greenhouse_board_state_{token}"
    cached_state = cache.get(cache_key)
    if cached_state is not None:
        return cached_state

    state = _read_board_state(token)
    # Failures are cached too. Without that, a Greenhouse outage makes every
    # careers page request wait out the full request timeout.
    timeout = (
        settings.GREENHOUSE_BOARD_CACHE_TIMEOUT
        if state in SUCCESS_STATES
        else settings.GREENHOUSE_BOARD_ERROR_CACHE_TIMEOUT
    )
    cache.set(cache_key, state, timeout)
    return state
