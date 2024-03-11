from collections import OrderedDict

from wagtail import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.telepath import register

from networkapi.wagtailpages.pagemodels.customblocks.common.base_link_block import (
    BaseLinkBlock,
    BaseLinkBlockAdapter,
    BaseLinkValue,
)


class LinkValue(BaseLinkValue):
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
        required=False,
        label="Link to",
    )
    file = DocumentChooserBlock(required=False, label="File")
    phone = blocks.CharBlock(max_length=30, required=False, label="Phone")

    label = blocks.CharBlock()

    new_window = blocks.BooleanBlock(label="Open in new window", required=False)

    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(local_blocks, **kwargs)
        # Reoder child_blocks so that label is first
        self.child_blocks = self.base_blocks.copy()
        child_blocks = OrderedDict(
            {
                "label": self.child_blocks.pop("label"),
            }
        )
        child_blocks.update({k: v for k, v in self.child_blocks.items()})
        self.child_blocks = child_blocks

    def get_default_values(self):
        default_values = super().get_default_values()
        default_values["file"] = None
        default_values["phone"] = ""
        return default_values

    class Meta:
        value_class = LinkValue
        icon = "link"
        template = "wagtailpages/blocks/link_block.html"


register(BaseLinkBlockAdapter(), BaseLinkBlock)
