from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock

from .link_block import OptionalLinkBlock


class ProductReviewCardBlock(BaseBlock):
    """
    A flexible card block for product reviews
    """

    product_review = blocks.PageChooserBlock(
        target_model="nothing_personal.NothingPersonalProductReviewPage",
        label="Product review selector",
        help_text="Select a Product Review",
    )

    class Meta:
        icon = "image"
        template_name = "product_review_card_block.html"
        label = "Product Review Card"


class ProductReviewCarouselBlock(BaseBlock):
    """
    Block container for displaying product review cards in a carousel.
    """

    subtitle = blocks.CharBlock(required=False, help_text="Optional subtitle for the contianer")
    title = blocks.CharBlock(required=False, help_text="Optional title for the container")
    text = blocks.RichTextBlock(required=False, help_text="Optional description text for the container")
    cta_link = OptionalLinkBlock(required=False, label="Link", help_text="Optional link for the container.")

    cards = blocks.StreamBlock(
        [
            ("product_review_card", ProductReviewCardBlock()),
        ],
        max_num=10,
        help_text="Maximum of 10 per carousel.",
    )

    class Meta:
        icon = "list-ul"
        template_name = "product_review_carousel_block.html"
        label = "Product Review Carousel"
