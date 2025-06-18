from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock

from .image_block import CustomImageBlock
from .link_block import LinkBlock


class ActivationCardBlock(BaseBlock):
    """
    A flexible card block for timely activations
    """

    topic = blocks.CharBlock(required=False, help_text="Optional topic tag for the card")
    category = blocks.CharBlock(required=False, help_text="Optional category for the card")
    title = blocks.CharBlock(required=True, help_text="Title for the card")
    text = blocks.RichTextBlock(required=False, help_text="Optional description text")
    image = CustomImageBlock(required=True)
    link = LinkBlock()

    class Meta:
        icon = "image"
        template_name = "activation_card_block.html"
        label = "Activation Card"


class TimelyActivationsCardsBlock(BaseBlock):
    """
    Block for displaying timely activations cards with customizable number of cards (1, 2, or 3)
    """

    title = blocks.CharBlock(required=False, help_text="Title for the activations section")

    # Display count selection
    card_count = blocks.ChoiceBlock(
        choices=[
            ("1", "One Card (Full Width)"),
            ("2", "Two Cards"),
            ("3", "Three Cards"),
        ],
        default="3",
        help_text="Select how many cards to display in a row",
    )

    cards = blocks.StreamBlock(
        [
            ("card", ActivationCardBlock()),
        ],
        min_num=1,
        max_num=3,
        help_text="Add between 1 and 3 cards. Only the number of cards selected above will be displayed.",
    )

    class Meta:
        icon = "list-ul"
        template_name = "timely_activations_cards_block.html"
        label = "Timely Activations Cards"
