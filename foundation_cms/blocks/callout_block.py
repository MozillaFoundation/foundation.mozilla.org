from wagtail.blocks import RichTextBlock

from foundation_cms.base.models.base_block import BaseBlock

from .decorators import skip_default_wrapper_on


@skip_default_wrapper_on("*")
class CalloutBlock(BaseBlock):

    heading = RichTextBlock(required=True, features=["h4", "h5", "h6"], help_text="Callout box title")
    description = RichTextBlock(required=True, help_text="Callout box content")

    class Meta:
        icon = "help"
        label = "Callout Box"
        template_name = "callout_block.html"
