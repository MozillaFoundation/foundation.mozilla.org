from wagtail.blocks import ChoiceBlock, RichTextBlock

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.constants import RICH_TEXT_FEATURES_NO_HEADINGS


class YesNoChoiceBlock(ChoiceBlock):
    """Choice block for Yes/No answers"""

    choices = [
        ("yes", "Yes"),
        ("no", "No"),
    ]


class ProductReviewSectionWhatYouShouldKnowBlock(BaseBlock):
    """Block for What You Should Know section with predefined questions"""

    trust_default_settings = YesNoChoiceBlock(required=False, help_text="Should I trust their default settings?")
    give_data_by_default = YesNoChoiceBlock(required=False, help_text="Should I give them my data by default?")
    use_offline = YesNoChoiceBlock(required=False, help_text="Can I use this product/service offline?")

    reconsider_buying = YesNoChoiceBlock(
        required=False,
        help_text="Should I reconsider buying this product because of this company's track record + data practices?",
    )
    reconsider_buying_explanation = RichTextBlock(
        required=False,
        help_text="Optional explanation for this answer",
        features=RICH_TEXT_FEATURES_NO_HEADINGS,
    )

    sells_user_data = YesNoChoiceBlock(
        required=False, help_text="Does this product/service sell or giveaway user data?"
    )
    sells_user_data_explanation = RichTextBlock(
        required=False, help_text="Optional explanation for this answer", features=RICH_TEXT_FEATURES_NO_HEADINGS
    )

    class Meta:
        template_name = "product_review_what_you_should_know_block.html"
        icon = "help"
        label = "What You Should Know"


class ProductReviewSectionReduceYourRisksBlock(BaseBlock):
    """Simple text block for Reduce Your Risks section"""

    content = RichTextBlock(help_text="Advice on how to reduce privacy risks", features=RICH_TEXT_FEATURES_NO_HEADINGS)

    class Meta:
        template_name = "product_review_reduce_your_risks_block.html"
        icon = "warning"
        label = "Reduce Your Risks"


class ProductReviewSectionGoodAndBadBlock(BaseBlock):
    """Block for The Good and The Bad section"""

    the_good = RichTextBlock(help_text="Positive aspects of this product", features=RICH_TEXT_FEATURES_NO_HEADINGS)
    the_bad = RichTextBlock(help_text="Negative aspects of this product", features=RICH_TEXT_FEATURES_NO_HEADINGS)

    class Meta:
        template_name = "product_review_good_and_bad_block.html"
        icon = "list-ul"
        label = "The Good and The Bad"


class ProductReviewSectionBottomLineBlock(BaseBlock):
    """Block for The Bottom Line section"""

    content = RichTextBlock(help_text="Final verdict and recommendation", features=RICH_TEXT_FEATURES_NO_HEADINGS)

    class Meta:
        template_name = "product_review_bottom_line_block.html"
        icon = "check"
        label = "The Bottom Line"
