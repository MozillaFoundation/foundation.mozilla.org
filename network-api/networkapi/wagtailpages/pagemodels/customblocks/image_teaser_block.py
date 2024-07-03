from django.forms.utils import ErrorList
from django.utils import functional as func_utils
from django.utils import text as text_utils
from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.images.blocks import ImageChooserBlock

from networkapi.wagtailpages.pagemodels.customblocks.link_button_block import (
    LinkButtonBlock,
)


class ImageTeaserValue(blocks.StructValue):
    @func_utils.cached_property
    def slug(self):
        return text_utils.slugify(self.get("title", ""))


class ImageTeaserBlock(blocks.StructBlock):
    title = blocks.CharBlock(help_text="Heading for the card.")
    text = blocks.RichTextBlock(features=["bold"])
    image = ImageChooserBlock()

    altText = blocks.CharBlock(required=True, help_text="Image description (for screen readers).")

    link_button = blocks.ListBlock(LinkButtonBlock(), min_num=0, max_num=1, help_text="Optional link button")
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
        top_divider = value.get("top_divider")
        bottom_divider = value.get("bottom_divider")
        if not top_divider and not bottom_divider:
            divider_styles = "tw-mt-8"
        if top_divider:
            divider_styles.append("tw-border-t tw-pt-24")
        if bottom_divider:
            divider_styles.append("tw-border-b tw-pb-24")
        context["divider_styles"] = " ".join(divider_styles)
        return context

    class Meta:
        label = "Image teaser"
        icon = "doc-full"
        template = "wagtailpages/blocks/image_teaser_block.html"
        value_class = ImageTeaserValue
