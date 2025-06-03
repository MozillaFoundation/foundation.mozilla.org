from wagtail.blocks import ChoiceBlock

from foundation_cms.base.models.base_block import BaseBlock


class SpacerBlock(BaseBlock):
    """
    A simple spacer block that can be used to create visual breaks in content with three size options.
    """

    size = ChoiceBlock(
        choices=[
            ("small", "Small"),
            ("medium", "Medium"),
            ("large", "Large"),
            ("xlarge", "Extra Large"),
        ],
        default="medium",
        help_text="Select the size of the spacer",
    )

    class Meta:
        template_name = "spacer_block.html"
        label = "Spacer"
