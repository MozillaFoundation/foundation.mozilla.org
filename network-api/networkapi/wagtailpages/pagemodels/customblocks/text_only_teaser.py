from django.forms.utils import ErrorList
from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockValidationError

from networkapi.wagtailpages.pagemodels.customblocks.link_block import (
    LinkWithoutLabelBlock,
)


class TextOnlyTeaserCard(blocks.StructBlock):
    heading = blocks.CharBlock(help_text="Heading for the card.")
    link_page = blocks.PageChooserBlock(required=False, help_text="Page that the header should link out to.")
    link_url = blocks.CharBlock(
        required=False,
        help_text="Optional URL that the header should link out to.",
    )
    link = blocks.ListBlock(
        LinkWithoutLabelBlock(), min_num=0, max_num=1, help_text="Optional link that the header should link out to."
    )
    meta_data = blocks.CharBlock(max_length=500)
    body = blocks.TextBlock(help_text="Body text of the card.", required=False, max_length=200)

    def clean(self, value):
        result = super().clean(value)
        if value["link_page"] and value["link_url"]:
            raise StructBlockValidationError(
                block_errors={"link_page": ErrorList(["Please choose between a link page OR a URL value."])}
            )

        return result


class TextOnlyTeaserBlock(blocks.StructBlock):
    cards = blocks.ListBlock(TextOnlyTeaserCard(), help_text="Please use a minimum of 3 cards.", min_num=3)

    class Meta:
        icon = "placeholder"
        template = "wagtailpages/blocks/text_only_teaser_block.html"
