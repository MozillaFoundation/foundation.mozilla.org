from wagtail import blocks

from foundation_cms.base.models.base_block import BaseBlock


class YesNoChoiceBlock(blocks.ChoiceBlock):
    """Choice block for Yes/No answers"""

    choices = [
        ("yes", "Yes"),
        ("no", "No"),
    ]


class WhatYouShouldKnowBlock(BaseBlock):
    """Block for What You Should Know section with predefined questions"""

    trust_default_settings = YesNoChoiceBlock(required=False, help_text="Should I trust their default settings?")
    give_data_by_default = YesNoChoiceBlock(required=False, help_text="Should I give them my data by default?")
    use_offline = YesNoChoiceBlock(required=False, help_text="Can I use this product/service offline?")

    reconsider_buying = YesNoChoiceBlock(
        required=False,
        help_text="Should I reconsider buying this product because of this company's track record + data practices?",
    )
    reconsider_buying_explanation = blocks.RichTextBlock(
        required=False, help_text="Optional explanation for this answer"
    )

    sells_user_data = YesNoChoiceBlock(
        required=False, help_text="Does this product/service sell or giveaway user data?"
    )
    sells_user_data_explanation = blocks.RichTextBlock(
        required=False, help_text="Optional explanation for this answer"
    )

    class Meta:
        template_name = "what_you_should_know_block.html"
        icon = "help-circle"
        label = "What You Should Know"


class ReduceYourRisksBlock(BaseBlock):
    """Simple text block for Reduce Your Risks section"""

    content = blocks.RichTextBlock(help_text="Advice on how to reduce privacy risks")

    class Meta:
        template_name = "reduce_your_risks_block.html"
        icon = "warning-sign"
        label = "Reduce Your Risks"


class GoodAndBadBlock(BaseBlock):
    """Block for The Good and The Bad section"""

    the_good = blocks.RichTextBlock(help_text="Positive aspects of this product")
    the_bad = blocks.RichTextBlock(help_text="Negative aspects of this product")

    class Meta:
        template_name = "good_and_bad_block.html"
        icon = "thumbs-up-down"
        label = "The Good and The Bad"


class BottomLineBlock(BaseBlock):
    """Block for The Bottom Line section"""

    content = blocks.RichTextBlock(help_text="Final verdict and recommendation")

    class Meta:
        template_name = "bottom_line_block.html"
        icon = "check-circle"
        label = "The Bottom Line"
