from django.conf import settings
from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.custom_rich_text_block import CustomRichTextBlock
from foundation_cms.blocks.greenhouse import (
    EMBED_SCRIPT_URL,
    HOSTED_BOARD_URL,
    STATE_BOARD,
    STATE_DEGRADED,
    STATE_EMPTY,
    get_greenhouse_board_state,
)


class GreenhouseBoardBlock(BaseBlock):
    empty_heading = blocks.CharBlock(
        required=False,
        max_length=100,
        default="No open roles right now",
        help_text="Shown when the job board has no open positions.",
    )
    empty_description = CustomRichTextBlock(
        required=False,
        default="<p>We don't have any openings at the moment. Please check back soon.</p>",
        help_text="Shown under the heading when there are no open positions.",
    )
    unavailable_heading = blocks.CharBlock(
        required=False,
        max_length=100,
        default="Our job board is temporarily unavailable",
        help_text="Shown when the job board cannot be loaded at all.",
    )
    unavailable_description = CustomRichTextBlock(
        required=False,
        default="<p>We're having trouble loading our open roles. Please try again shortly.</p>",
        help_text="Shown under the heading when the job board cannot be loaded at all.",
    )
    hosted_board_notice = blocks.CharBlock(
        required=False,
        max_length=140,
        default="Not seeing our open roles?",
        help_text="Shown under the job board, followed by the link below.",
    )
    hosted_board_link_label = blocks.CharBlock(
        required=False,
        max_length=60,
        default="View them on Greenhouse",
        help_text="Label for the link to the Greenhouse-hosted board.",
    )

    class Meta:
        template_name = "greenhouse_board_block.html"
        icon = "list-ul"
        label = "Greenhouse Job Board"
        description = "Embeds the Greenhouse job board. Only one per page: the embed uses a fixed element id."

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        # The token stays a setting rather than a block field: a typo would take
        # the page down, and a text field in this page's translatable body would
        # reach translators as a string to translate.
        token = settings.GREENHOUSE_BOARD_TOKEN
        state = get_greenhouse_board_state(token)
        context["board_state"] = state

        if state in (STATE_BOARD, STATE_DEGRADED):
            context["embed_script_url"] = EMBED_SCRIPT_URL.format(token=token)
            # Offered whenever we embed: every state we detect is server-side, so
            # an embed blocked by CSP or an ad blocker leaves no other way out.
            context["hosted_board_url"] = HOSTED_BOARD_URL.format(token=token)
        elif state == STATE_EMPTY:
            context["panel_heading"] = value["empty_heading"]
            context["panel_description"] = value["empty_description"]
        else:
            context["panel_heading"] = value["unavailable_heading"]
            context["panel_description"] = value["unavailable_description"]

        return context
