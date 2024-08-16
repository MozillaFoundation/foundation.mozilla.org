from wagtail import blocks

from ..customblocks.full_content_rich_text_options import full_content_rich_text_options
from .image_block import ImageBlock
from .link_block import LinkWithoutLabelBlock


class ImageTextBlock(ImageBlock):
    text = blocks.RichTextBlock(features=full_content_rich_text_options)
    url = blocks.ListBlock(
        LinkWithoutLabelBlock(), min_num=0, max_num=1, help_text="Optional URL that this image should link out to."
    )
    top_divider = blocks.BooleanBlock(
        required=False,
        help_text="Optional divider above content block.",
    )
    bottom_divider = blocks.BooleanBlock(
        required=False,
        help_text="Optional divider below content block.",
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        divider_styles = []
        if value.get("top_divider"):
            divider_styles.append("div-top pt-4")
        if value.get("bottom_divider"):
            divider_styles.append("div-bottom pb-4")
        context["divider_styles"] = " ".join(divider_styles)
        return context

    class Meta:
        icon = "doc-full"
        template = "wagtailpages/blocks/image_text.html"
