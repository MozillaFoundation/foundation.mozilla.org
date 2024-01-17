from django.forms.utils import ErrorList
from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.images.blocks import ImageChooserBlock

from networkapi.wagtailpages.pagemodels.customblocks.base_rich_text_options import (
    base_rich_text_options,
)


class NoticeBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    image_alt_text = blocks.CharBlock(required=False, help_text="Image description (for screen readers).")
    text = blocks.RichTextBlock(features=base_rich_text_options)

    class Meta:
        icon = "doc-full"
        template = "donate/blocks/notice_block.html"

    def clean(self, value):
        cleaned_data = super().clean(value)
        errors = {}

        if cleaned_data["image"] and not cleaned_data["image_alt_text"]:
            errors["image"] = ErrorList(["Image must include alt text."])
        if cleaned_data["image_alt_text"] and not cleaned_data["image"]:
            errors["image_alt_text"] = ErrorList(["Alt text must have an associated image."])
        if errors:
            raise StructBlockValidationError(errors)

        return cleaned_data
