from wagtail.blocks import CharBlock, ListBlock, StreamBlock

from foundation_cms.base.models.base_block import BaseBlock
from foundation_cms.blocks.custom_rich_text_block import CustomRichTextBlock
from foundation_cms.constants import RICH_TEXT_FEATURES_NO_HEADINGS


class AccordionBlockItem(BaseBlock):
    title = CharBlock(required=True, help_text="Heading for the Accordion Item")
    content = StreamBlock(
        [
            ("rich_text", CustomRichTextBlock(features=RICH_TEXT_FEATURES_NO_HEADINGS)),
        ],
        required=False,
        use_json_field=True,
    )

    class Meta:
        label = "Accordion Item"
        icon = "arrow-down-big"
        template_name = "accordion_block_item.html"


class AccordionBlock(BaseBlock):
    accordion_items = ListBlock(AccordionBlockItem(), min_num=1)

    class Meta:
        label = "Accordion"
        icon = "form"
        template_name = "accordion_block.html"
