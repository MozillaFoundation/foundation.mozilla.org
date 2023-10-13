from django.core.exceptions import ValidationError
from wagtail.core import blocks
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
        image = cleaned_data.get("image")
        image_alt_text = cleaned_data.get("image_alt_text")

        if image and not image_alt_text:
            error_msg = "Image must include alt text."
            raise ValidationError(
                {
                    "image_alt_text": ValidationError(error_msg),
                }
            )

        if image_alt_text and not image:
            error_msg = "Alt text must have an associated image."
            raise ValidationError(
                {
                    "image": ValidationError(error_msg),
                }
            )

        return cleaned_data
