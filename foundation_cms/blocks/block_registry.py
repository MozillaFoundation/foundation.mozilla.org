from django.conf import settings
from wagtail.blocks import RichTextBlock

from .accordion_block import AccordionBlock
from .callout_block import CalloutBlock
from .divider_block import DividerBlock
from .featured_card_block import FeaturedCardBlock
from .featured_container_block import FeaturedContainerBlock
from .fru_element_block import FruElementBlock
from .iframe_block import iFrameBlock
from .image_block import CustomImageBlock
from .impact_number_block import ImpactNumberBlock
from .link_button_block import LinkButtonBlock
from .list_block import ListBlock
from .media_block import CustomMediaBlock
from .newsletter_signup_block import NewsletterSignupBlock
from .newsletter_unsubscribe_block import NewsletterUnsubscribeBlock
from .pillar_card_set_block import PillarCardSetBlock
from .podcast_block import PodcastBlock
from .portrait_card_set_block import PortraitCardSetBlock
from .quote_block import QuoteBlock
from .spacer_block import SpacerBlock
from .spotlight_card_set_block import SpotlightCardSetBlock
from .tabbed_content_container_block import TabbedContentContainerBlock
from .timely_activations_cards_block import TimelyActivationsCardsBlock
from .title_block import TitleBlock
from .two_column_container_block import TwoColumnContainerBlock
from .video_block import VideoBlock


class BlockGroups:
    CARDS = "Card Collections"
    DATA = "Data Display"
    ENGAGEMENT = "Engagement & Buttons"
    LAYOUT = "Layout"
    MEDIA = "Media & Embeds"
    TEXT = "Text"


class BlockRegistry:
    """Registry for all StreamField blocks with their configs."""

    BLOCKS = {
        # Card Collections
        "featured_card_block": {
            "class": FeaturedCardBlock,
            "kwargs": {"skip_default_wrapper": True},
            "group": BlockGroups.CARDS,
        },
        "pillar_card_set": {
            "class": PillarCardSetBlock,
            "group": BlockGroups.CARDS,
        },
        "portrait_card_set_block": {
            "class": PortraitCardSetBlock,
            "kwargs": {"skip_default_wrapper": True},
            "group": BlockGroups.CARDS,
        },
        "spotlight_card_set_block": {
            "class": SpotlightCardSetBlock,
            "kwargs": {"skip_default_wrapper": True},
            "group": BlockGroups.CARDS,
        },
        "tabbed_content": {
            "class": TabbedContentContainerBlock,
            "group": BlockGroups.CARDS,
        },
        "timely_activations_cards": {
            "class": TimelyActivationsCardsBlock,
            "group": BlockGroups.CARDS,
        },
        # Data Display
        "impact_numbers": {
            "class": ImpactNumberBlock,
            "group": BlockGroups.DATA,
        },
        "list_block": {
            "class": ListBlock,
            "group": BlockGroups.DATA,
        },
        # Engagement
        "fru_element_block": {
            "class": FruElementBlock,
            "group": BlockGroups.ENGAGEMENT,
        },
        "link_button_block": {
            "class": LinkButtonBlock,
            "group": BlockGroups.ENGAGEMENT,
        },
        "newsletter_signup": {
            "class": NewsletterSignupBlock,
            "group": BlockGroups.ENGAGEMENT,
        },
        "newsletter_unsubscribe": {
            "class": NewsletterUnsubscribeBlock,
            "group": BlockGroups.ENGAGEMENT,
        },
        # Layout
        "divider": {
            "class": DividerBlock,
            "group": BlockGroups.LAYOUT,
        },
        "featured_container": {
            "class": FeaturedContainerBlock,
            "group": BlockGroups.LAYOUT,
        },
        "spacer_block": {
            "class": SpacerBlock,
            "group": BlockGroups.LAYOUT,
        },
        "two_column_container_block": {
            "class": TwoColumnContainerBlock,
            "group": BlockGroups.LAYOUT,
        },
        # Media & Embeds
        "custom_media": {
            "class": CustomMediaBlock,
            "group": BlockGroups.MEDIA,
        },
        "iframe_block": {
            "class": iFrameBlock,
            "group": BlockGroups.MEDIA,
        },
        "image": {
            "class": CustomImageBlock,
            "group": BlockGroups.MEDIA,
        },
        "podcast_block": {
            "class": PodcastBlock,
            "group": BlockGroups.MEDIA,
        },
        "video_block": {
            "class": VideoBlock,
            "group": BlockGroups.MEDIA,
        },
        # Text
        "accordion_block": {
            "class": AccordionBlock,
            "group": BlockGroups.TEXT,
        },
        "callout": {
            "class": CalloutBlock,
            "kwargs": {"skip_default_wrapper": True},
            "group": BlockGroups.TEXT,
        },
        "quote": {
            "class": QuoteBlock,
            "group": BlockGroups.TEXT,
        },
        "rich_text": {
            "class": RichTextBlock,
            "kwargs": {"template": "patterns/blocks/themes/default/rich_text_block.html"},
            "group": BlockGroups.TEXT,
        },
        "title_block": {
            "class": TitleBlock,
            "group": BlockGroups.TEXT,
        },
    }

    @classmethod
    def get_blocks(cls, block_names):
        """
        Get block instances for the specified block names.
        Example:
            blocks = BlockRegistry.get_blocks(["rich_text", "image"])
            # Returns: [("rich_text", RichTextBlock(...)), ("image", CustomImageBlock(...))]
        """
        blocks = []

        for name in block_names:
            if name not in cls.BLOCKS:
                if settings.DEBUG:
                    raise KeyError(f"Block '{name}' not registered in BlockRegistry.BLOCKS")
                continue

            block_info = cls.BLOCKS[name]

            if "kwargs" in block_info:
                # block has special kwargs (e.g., skip_default_wrapper)
                block = block_info["class"](group=block_info["group"], **block_info["kwargs"])
            else:
                block = block_info["class"](group=block_info["group"])

            blocks.append((name, block))

        return blocks
