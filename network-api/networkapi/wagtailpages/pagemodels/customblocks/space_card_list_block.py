from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.blocks.struct_block import StructBlockValidationError

from django.forms.utils import ErrorList


class SpaceCardBlockStructValue(blocks.StructValue):
    @property
    def link(self):
        link_url = self.get('link_url')
        link_page = self.get('link_page')

        if link_url:
            return link_url
        elif link_page:
            return link_page.url


class SpaceCardBlock(blocks.StructBlock):
    image = ImageChooserBlock()

    title = blocks.CharBlock(
        help_text='Heading for the card.'
    )

    body = blocks.TextBlock(
        help_text='Body text of the card.'
    )

    link_page = blocks.PageChooserBlock(
        required=False,
        help_text='Page that this card should link out to.',
    )

    link_url = blocks.URLBlock(
        required=False,
        help_text='URL that this card should link out to.',
    )

    def clean(self, value):
        errors = {}

        link_page = value.get('link_page')
        link_url = value.get('link_url')

        if (link_page and link_url) or (not link_page and not link_url):
            errors['link_page'] = ErrorList(['Please specify either a link page or a link URL.'])
            errors['link_url'] = ErrorList(['Please specify either a link page or a link URL.'])

        if errors:
            raise StructBlockValidationError(errors)

        return super().clean(value)

    class Meta:
        value_class = SpaceCardBlockStructValue


class SpaceCardListBlock(blocks.StructBlock):
    space_cards = blocks.ListBlock(SpaceCardBlock())

    class Meta:
        icon = 'placeholder'
        template = 'wagtailpages/blocks/space_card_list_block.html'
