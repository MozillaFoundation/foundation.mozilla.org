from unittest.mock import Mock, patch

import requests
from django.core.cache import cache
from django.test import SimpleTestCase, override_settings

from foundation_cms.blocks.greenhouse import (
    REQUEST_TIMEOUT,
    STATE_BOARD,
    STATE_DEGRADED,
    STATE_EMPTY,
    STATE_UNAVAILABLE,
    get_greenhouse_board_state,
)

DUMMY_CACHE = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

GREENHOUSE_LOGGER = "foundation_cms.blocks.greenhouse"


def build_response(status_code=200, payload=None, json_error=None):
    response = Mock()
    response.status_code = status_code
    if json_error is not None:
        response.json.side_effect = json_error
    else:
        response.json.return_value = payload
    return response


@override_settings(CACHES=DUMMY_CACHE)
@patch("foundation_cms.blocks.greenhouse.requests.get")
class GetGreenhouseBoardStateTests(SimpleTestCase):
    """Caching is off here so every test exercises a real lookup."""

    def test_open_jobs_return_the_board_state(self, mock_get):
        mock_get.return_value = build_response(payload={"jobs": [{"id": 1}, {"id": 2}]})

        self.assertEqual(get_greenhouse_board_state("mozilla"), STATE_BOARD)

    def test_zero_open_jobs_returns_the_empty_state(self, mock_get):
        mock_get.return_value = build_response(payload={"jobs": []})

        self.assertEqual(get_greenhouse_board_state("mozilla"), STATE_EMPTY)

    def test_timeout_returns_the_degraded_state(self, mock_get):
        mock_get.side_effect = requests.Timeout

        self.assertEqual(get_greenhouse_board_state("mozilla"), STATE_DEGRADED)

    def test_connection_error_returns_the_degraded_state(self, mock_get):
        mock_get.side_effect = requests.ConnectionError

        self.assertEqual(get_greenhouse_board_state("mozilla"), STATE_DEGRADED)

    def test_server_error_returns_the_degraded_state(self, mock_get):
        mock_get.return_value = build_response(status_code=503)

        self.assertEqual(get_greenhouse_board_state("mozilla"), STATE_DEGRADED)

    def test_malformed_json_returns_the_degraded_state(self, mock_get):
        mock_get.return_value = build_response(json_error=ValueError)

        self.assertEqual(get_greenhouse_board_state("mozilla"), STATE_DEGRADED)

    def test_payload_without_a_jobs_key_returns_the_degraded_state(self, mock_get):
        mock_get.return_value = build_response(payload={"meta": {"total": 3}})

        self.assertEqual(get_greenhouse_board_state("mozilla"), STATE_DEGRADED)

    def test_payload_with_a_non_list_jobs_value_returns_the_degraded_state(self, mock_get):
        mock_get.return_value = build_response(payload={"jobs": 3})

        self.assertEqual(get_greenhouse_board_state("mozilla"), STATE_DEGRADED)

    def test_unknown_token_returns_the_unavailable_state_and_logs_an_error(self, mock_get):
        mock_get.return_value = build_response(status_code=404)

        with self.assertLogs(GREENHOUSE_LOGGER, level="ERROR") as logs:
            state = get_greenhouse_board_state("not-a-real-board")

        self.assertEqual(state, STATE_UNAVAILABLE)
        self.assertIn("not-a-real-board", logs.output[0])

    def test_unset_token_returns_the_unavailable_state_without_calling_greenhouse(self, mock_get):
        with self.assertLogs(GREENHOUSE_LOGGER, level="WARNING"):
            state = get_greenhouse_board_state("")

        self.assertEqual(state, STATE_UNAVAILABLE)
        mock_get.assert_not_called()

    def test_requests_use_a_bounded_timeout(self, mock_get):
        mock_get.return_value = build_response(payload={"jobs": []})

        get_greenhouse_board_state("mozilla")

        self.assertEqual(mock_get.call_args.kwargs["timeout"], REQUEST_TIMEOUT)


@override_settings(GREENHOUSE_BOARD_CACHE_TIMEOUT=300, GREENHOUSE_BOARD_ERROR_CACHE_TIMEOUT=60)
@patch("foundation_cms.blocks.greenhouse.requests.get")
class GreenhouseBoardStateCachingTests(SimpleTestCase):
    def setUp(self):
        cache.clear()

    def tearDown(self):
        cache.clear()

    def test_repeated_calls_hit_greenhouse_only_once(self, mock_get):
        mock_get.return_value = build_response(payload={"jobs": [{"id": 1}]})

        get_greenhouse_board_state("mozilla")
        get_greenhouse_board_state("mozilla")

        self.assertEqual(mock_get.call_count, 1)

    def test_separate_tokens_are_cached_separately(self, mock_get):
        mock_get.return_value = build_response(payload={"jobs": [{"id": 1}]})

        get_greenhouse_board_state("mozilla")
        get_greenhouse_board_state("some-other-board")

        self.assertEqual(mock_get.call_count, 2)

    def test_a_successful_state_is_cached_with_the_success_timeout(self, mock_get):
        mock_get.return_value = build_response(payload={"jobs": [{"id": 1}]})

        with patch("foundation_cms.blocks.greenhouse.cache.set") as mock_set:
            get_greenhouse_board_state("mozilla")

        self.assertEqual(mock_set.call_args.args, ("greenhouse_board_state_mozilla", STATE_BOARD, 300))

    def test_a_degraded_state_is_cached_with_the_shorter_error_timeout(self, mock_get):
        mock_get.side_effect = requests.Timeout

        with patch("foundation_cms.blocks.greenhouse.cache.set") as mock_set:
            get_greenhouse_board_state("mozilla")

        self.assertEqual(mock_set.call_args.args, ("greenhouse_board_state_mozilla", STATE_DEGRADED, 60))

    def test_an_unavailable_state_is_cached_with_the_shorter_error_timeout(self, mock_get):
        mock_get.return_value = build_response(status_code=404)

        with self.assertLogs(GREENHOUSE_LOGGER, level="ERROR"):
            with patch("foundation_cms.blocks.greenhouse.cache.set") as mock_set:
                get_greenhouse_board_state("mozilla")

        self.assertEqual(mock_set.call_args.args, ("greenhouse_board_state_mozilla", STATE_UNAVAILABLE, 60))

    def test_an_unset_token_is_never_cached(self, mock_get):
        with patch("foundation_cms.blocks.greenhouse.cache.set") as mock_set:
            with self.assertLogs(GREENHOUSE_LOGGER, level="WARNING"):
                get_greenhouse_board_state("")

        mock_set.assert_not_called()
