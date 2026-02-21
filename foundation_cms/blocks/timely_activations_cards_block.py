from wagtail import blocks
from wagtail.images.blocks import ImageBlock

from foundation_cms.base.models.base_block import BaseBlock

from .custom_rich_text_block import CustomRichTextBlock
from .link_block import LinkBlock


class ActivationCardBlock(BaseBlock):
    """
    A flexible card block for timely activations
    """

    category = blocks.CharBlock(required=False, help_text="Optional category for the card")
    title = blocks.CharBlock(required=True, help_text="Title for the card")
    text = CustomRichTextBlock(required=False, help_text="Optional description text")
    image = ImageBlock(required=True)
    link = LinkBlock()

    class Meta:
        icon = "image"
        template_name = "activation_card_block.html"
        label = "Activation Card"


class TimelyActivationsCardsBlock(BaseBlock):
    """
    Block for displaying timely activations cards with customizable number of cards (1, 2, or 3)
    """

    cards = blocks.StreamBlock(
        [
            ("card", ActivationCardBlock()),
        ],
        min_num=1,
        max_num=3,
        help_text="Add between 1 and 3 cards.",
    )

    class Meta:
        icon = "list-ul"
        template_name = "timely_activations_cards_block.html"
        label = "Timely Activations Cards"
