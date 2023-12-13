from django.forms.utils import ErrorList
from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.images.blocks import ImageChooserBlock


class ListingCard(blocks.StructBlock):
    image = ImageChooserBlock()

    alt_text = blocks.CharBlock(required=False, help_text="Alt text for card's image.")

    title = blocks.CharBlock(help_text="Heading for the card.")
    category = blocks.CharBlock(help_text="Category text for the card.", required=False)
    date_meta = blocks.CharBlock(help_text="Date and time or other information.", required=False)

    body = blocks.RichTextBlock(features=["bold"], help_text="Body text of the card.", required=False)

    link_page = blocks.PageChooserBlock(required=False, help_text="Page that this should link out to.")

    link_url = blocks.CharBlock(
        required=False,
        help_text="Optional URL that the header should link out to.",
    )

    def clean(self, value):
        result = super().clean(value)
        if value["link_page"] and value["link_url"]:
            raise StructBlockValidationError(
                {"link_page": ErrorList(["Please choose between a link page OR a URL value."])}
            )

        return result


class ListingBlock(blocks.StructBlock):
    heading = blocks.CharBlock(help_text="Heading for the block.", required=False)

    cards = blocks.ListBlock(ListingCard(), help_text="Please use a minimum of 2 cards.", min_num=2)

    class Meta:
        icon = "placeholder"
        template = "wagtailpages/blocks/listing_block.html"
