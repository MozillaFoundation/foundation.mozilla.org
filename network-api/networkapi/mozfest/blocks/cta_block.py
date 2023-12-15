from django.forms.utils import ErrorList
from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockValidationError


class CTABlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    text = blocks.CharBlock(required=False)
    link_url = blocks.URLBlock(required=False)
    link_text = blocks.CharBlock(required=False, max_length=50)

    class Meta:
        template = "fragments/blocks/cta_block.html"
        label = "Call to action"

    def clean(self, value):
        result = super().clean(value)

        link_url = value.get("link_url")
        link_text = value.get("link_text")

        if link_url and not link_text:
            raise StructBlockValidationError({"link_text": ErrorList(["Please add a text value for the link."])})

        if link_text and not link_url:
            raise StructBlockValidationError({"link_url": ErrorList(["Please add a URL value for the link."])})

        return result
