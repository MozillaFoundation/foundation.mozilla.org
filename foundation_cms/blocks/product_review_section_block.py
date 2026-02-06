from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.custom_rich_text_block import CustomRichTextBlock
from foundation_cms.constants import RICH_TEXT_FEATURES_NO_HEADINGS


class ProductReviewSectionWhatYouShouldKnowBlock(BaseBlock):
    """Block for What You Should Know section with predefined questions"""

    trust_default_settings = CustomRichTextBlock(
        required=False,
        help_text="Should I trust their default settings?",
        features=RICH_TEXT_FEATURES_NO_HEADINGS,
    )
    what_personal_data_they_have = CustomRichTextBlock(
        required=False,
        help_text="What personal data do they have?",
        features=RICH_TEXT_FEATURES_NO_HEADINGS,
    )
    track_record = CustomRichTextBlock(
        required=False,
        help_text="Track record",
        features=RICH_TEXT_FEATURES_NO_HEADINGS,
    )
    sells_or_shares_user_data = CustomRichTextBlock(
        required=False,
        help_text="Does this product sell or share user data?",
        features=RICH_TEXT_FEATURES_NO_HEADINGS,
    )

    class Meta:
        template_name = "product_review_what_you_should_know_block.html"
        icon = "help"
        label = "What You Should Know"


class ProductReviewSectionReduceYourRisksBlock(BaseBlock):
    """Simple text block for Reduce Your Risks section"""

    content = CustomRichTextBlock(
        help_text="Advice on how to reduce privacy risks", features=RICH_TEXT_FEATURES_NO_HEADINGS
    )

    class Meta:
        template_name = "product_review_reduce_your_risks_block.html"
        icon = "warning"
        label = "Reduce Your Risks"


class ProductReviewSectionGoodAndBadBlock(BaseBlock):
    """Block for The Good and The Bad section"""

    the_good = CustomRichTextBlock(
        help_text="Positive aspects of this product", features=RICH_TEXT_FEATURES_NO_HEADINGS
    )
    the_bad = CustomRichTextBlock(
        help_text="Negative aspects of this product", features=RICH_TEXT_FEATURES_NO_HEADINGS
    )

    class Meta:
        template_name = "product_review_good_and_bad_block.html"
        icon = "list-ul"
        label = "The Good and The Bad"


class ProductReviewSectionBottomLineBlock(BaseBlock):
    """Block for The Bottom Line section"""

    content = CustomRichTextBlock(
        help_text="Final verdict and recommendation", features=RICH_TEXT_FEATURES_NO_HEADINGS
    )

    class Meta:
        template_name = "product_review_bottom_line_block.html"
        icon = "check"
        label = "The Bottom Line"
