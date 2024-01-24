from django.forms.utils import ErrorList
from django.utils import functional as func_utils
from django.utils import text as text_utils
from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.images.blocks import ImageChooserBlock


class ImageTeaserValue(blocks.StructValue):
    @func_utils.cached_property
    def slug(self):
        return text_utils.slugify(self.get("title", ""))


class ImageTeaserBlock(blocks.StructBlock):
    title = blocks.CharBlock(help_text="Heading for the card.")
    text = blocks.RichTextBlock(features=["bold"])
    image = ImageChooserBlock()

    altText = blocks.CharBlock(required=True, help_text="Image description (for screen readers).")

    url_label = blocks.CharBlock(required=False)
    url = blocks.CharBlock(required=False)
    styling = blocks.ChoiceBlock(
        choices=[
            ("btn-primary", "Primary button"),
            ("btn-secondary", "Secondary button"),
        ],
        default="btn-primary",
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

    def clean(self, value):
        result = super().clean(value)
        errors = {}

        if value["url"] and not value["url_label"]:
            errors["url_label"] = ErrorList(["Please add a label value for the URL."])
        if value["url_label"] and not value["url"]:
            errors["url"] = ErrorList(["Please add a URL value for the link."])
        if errors:
            raise StructBlockValidationError(block_errors=errors)

        return result

    class Meta:
        label = "Image teaser"
        icon = "doc-full"
        template = "wagtailpages/blocks/image_teaser_block.html"
        value_class = ImageTeaserValue
