from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.telepath import register

from foundation_cms.blocks.common.link_block.base_link_block import (
    BaseLinkBlock,
    BaseLinkBlockAdapter,
    BaseLinkValue,
)
from foundation_cms.validators import AnchorLinkValidator


class LinkValue(BaseLinkValue):
    def get_email_link(self):
        return f"mailto:{self.get('email')}"

    def get_anchor_link(self):
        return f"#{self.get('anchor')}"

    def get_phone_link(self):
        return "tel:{}".format(self.get("phone"))

    def get_file_link(self):
        file = self.get("file")
        return file.url if file else None


class LinkBlock(BaseLinkBlock):
    link_to = blocks.ChoiceBlock(
        choices=[
            ("page", "Page"),
            ("external_url", "External URL"),
            ("relative_url", "Relative URL"),
            ("email", "Email"),
            ("anchor", "Anchor"),
            ("file", "File"),
            ("phone", "Phone"),
        ],
        label="Link to",
    )
    anchor = blocks.CharBlock(
        max_length=300,
        required=False,
        validators=[AnchorLinkValidator()],
        label="#",
        help_text='An id attribute of an element on the current page. For example, "#section-1"',
    )
    email = blocks.EmailBlock(required=False)
    file = DocumentChooserBlock(required=False, label="File")
    phone = blocks.CharBlock(max_length=30, required=False, label="Phone")

    new_window = blocks.BooleanBlock(label="Open in new window", required=False)

    def get_default_values(self):
        default_values = super().get_default_values()
        default_values["anchor"] = ""
        default_values["email"] = ""
        default_values["file"] = None
        default_values["phone"] = ""
        return default_values

    class Meta:
        value_class = LinkValue
        icon = "link"
        template = "wagtailpages/blocks/link_block.html"


register(BaseLinkBlockAdapter(), LinkBlock)


class LinkWithoutLabelBlock(LinkBlock):
    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(local_blocks, **kwargs)
        self.child_blocks = self.base_blocks.copy()
        self.child_blocks.pop("label")


class OptionalLinkBlock(blocks.ListBlock):
    """
    A wrapper for a single optional LinkBlock, useful for conditional display.
    Use `self.YOUR_FIELD_NAME.0` in templates if present.
    """

    def __init__(self, **kwargs):
        super().__init__(LinkBlock(), min_num=0, max_num=1, **kwargs)

    def get_default(self):
        # Ensures the field starts truly empty, not with a blank block
        return []

    class Meta:
        label = "Optional Link"


register(BaseLinkBlockAdapter(), LinkWithoutLabelBlock)
