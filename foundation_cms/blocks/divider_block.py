from foundation_cms.base.models.base_block import BaseBlock


class DividerBlock(BaseBlock):
    """
    A simple divider block that can be used to create visual breaks in content.
    """

    class Meta:
        template_name = "divider_block.html"
        icon = "minus"
        label = "Divider"
