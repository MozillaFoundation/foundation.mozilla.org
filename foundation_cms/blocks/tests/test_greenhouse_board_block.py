from unittest.mock import patch

from django.test import RequestFactory, TestCase, override_settings
from wagtail.blocks import StreamBlockValidationError

from foundation_cms.base.models.abstract_base_page import BASE_BLOCK_NAMES
from foundation_cms.base.models.abstract_general_page import GENERAL_PAGE_BLOCK_NAMES
from foundation_cms.blocks.greenhouse import (
    STATE_BOARD,
    STATE_DEGRADED,
    STATE_EMPTY,
    STATE_UNAVAILABLE,
)
from foundation_cms.blocks.greenhouse_board_block import GreenhouseBoardBlock
from foundation_cms.core.models import GeneralPage

EMBED_SCRIPT = "https://boards.greenhouse.io/embed/job_board/js?for=mozilla"
HOSTED_BOARD = "https://job-boards.greenhouse.io/mozilla"

COPY = {
    "empty_heading": "No open roles right now",
    "empty_description": "<p>Check back soon.</p>",
    "unavailable_heading": "Our job board is temporarily unavailable",
    "unavailable_description": "<p>Try again shortly.</p>",
    "hosted_board_notice": "Not seeing our open roles?",
    "hosted_board_link_label": "View them on Greenhouse",
}


@override_settings(GREENHOUSE_BOARD_TOKEN="mozilla")
@patch("foundation_cms.blocks.greenhouse_board_block.get_greenhouse_board_state")
class GreenhouseBoardBlockRenderTests(TestCase):
    def render(self, copy=None, **context):
        block = GreenhouseBoardBlock()
        value = block.to_python({**COPY, **(copy or {})})
        return block.render(value, context={"theme": "default", **context})

    def test_board_state_renders_the_embed(self, mock_state):
        mock_state.return_value = STATE_BOARD

        html = self.render()

        self.assertIn('id="grnhse_app"', html)
        self.assertIn(EMBED_SCRIPT, html)

    def test_the_embed_script_carries_the_csp_nonce(self, mock_state):
        mock_state.return_value = STATE_BOARD
        request = RequestFactory().get("/careers/")
        request.csp_nonce = "test-nonce"

        html = self.render(request=request)

        self.assertIn('nonce="test-nonce"', html)

    def test_board_state_renders_the_hosted_board_link_but_no_fallback_panel(self, mock_state):
        mock_state.return_value = STATE_BOARD

        html = self.render()

        self.assertNotIn("greenhouse-board-block__panel", html)
        self.assertIn(HOSTED_BOARD, html)

    def test_empty_state_renders_the_no_roles_panel_instead_of_the_embed(self, mock_state):
        mock_state.return_value = STATE_EMPTY

        html = self.render()

        self.assertIn("greenhouse-board-block__panel--empty", html)
        self.assertIn("No open roles right now", html)
        self.assertNotIn("grnhse_app", html)

    def test_degraded_state_renders_the_embed_alongside_a_link_to_the_hosted_board(self, mock_state):
        mock_state.return_value = STATE_DEGRADED

        html = self.render()

        self.assertIn('id="grnhse_app"', html)
        self.assertIn(EMBED_SCRIPT, html)
        self.assertIn(HOSTED_BOARD, html)
        self.assertIn("View them on Greenhouse", html)
        self.assertNotIn("greenhouse-board-block__panel", html)

    def test_the_hosted_board_link_opens_in_a_new_tab_safely(self, mock_state):
        mock_state.return_value = STATE_DEGRADED

        html = self.render()

        self.assertIn('rel="noopener noreferrer"', html)

    def test_unavailable_state_renders_the_panel_without_a_link(self, mock_state):
        mock_state.return_value = STATE_UNAVAILABLE

        html = self.render()

        self.assertIn("greenhouse-board-block__panel--unavailable", html)
        self.assertIn("Our job board is temporarily unavailable", html)
        self.assertNotIn("grnhse_app", html)
        self.assertNotIn("job-boards.greenhouse.io", html)

    def test_blank_fallback_copy_renders_no_heading_or_description(self, mock_state):
        mock_state.return_value = STATE_EMPTY

        html = self.render(copy={"empty_heading": "", "empty_description": ""})

        self.assertIn("greenhouse-board-block__panel--empty", html)
        self.assertNotIn("greenhouse-board-block__panel-heading", html)
        self.assertNotIn("greenhouse-board-block__panel-description", html)

    def test_blank_hosted_board_copy_renders_no_notice(self, mock_state):
        mock_state.return_value = STATE_DEGRADED

        html = self.render(copy={"hosted_board_notice": "", "hosted_board_link_label": ""})

        self.assertIn('id="grnhse_app"', html)
        self.assertNotIn("greenhouse-board-block__notice", html)

    def test_the_block_exposes_the_state_as_a_data_attribute(self, mock_state):
        mock_state.return_value = STATE_EMPTY

        html = self.render()

        self.assertIn('data-board-state="empty"', html)

    def test_the_token_is_read_from_settings_not_from_editor_input(self, mock_state):
        mock_state.return_value = STATE_BOARD

        self.render()

        mock_state.assert_called_once_with("mozilla")


class GreenhouseBoardBlockConfigurationTests(TestCase):
    def test_the_block_declares_the_expected_child_blocks(self):
        self.assertEqual(set(GreenhouseBoardBlock().child_blocks), set(COPY))

    def test_the_block_is_available_on_general_pages_only(self):
        self.assertIn("greenhouse_board", GENERAL_PAGE_BLOCK_NAMES)
        self.assertNotIn("greenhouse_board", BASE_BLOCK_NAMES)

    def test_a_general_page_accepts_a_single_board(self):
        stream_block = GeneralPage.body.field.stream_block
        one_board = stream_block.to_python([{"type": "greenhouse_board", "value": COPY}])

        stream_block.clean(one_board)

    def test_a_general_page_rejects_a_second_board(self):
        stream_block = GeneralPage.body.field.stream_block
        two_boards = stream_block.to_python([{"type": "greenhouse_board", "value": COPY} for _ in range(2)])

        with self.assertRaises(StreamBlockValidationError) as raised:
            stream_block.clean(two_boards)

        self.assertIn("maximum number of items is 1", raised.exception.non_block_errors.as_text())
