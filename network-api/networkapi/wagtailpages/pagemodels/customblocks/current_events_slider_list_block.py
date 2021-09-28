from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class CurrentEventBaseButtonBlock(blocks.StructBlock):
    label = blocks.CharBlock(help_text='Button label')


class CurrentEventButtonInternalPage(CurrentEventBaseButtonBlock):
    link = blocks.PageChooserBlock(help_text='Page that this button should link out to.')


class CurrentEventButtonExternalPage(CurrentEventBaseButtonBlock):
    link = blocks.URLBlock(help_text='URL that this button should link out to.')


class CurrentEventBlockStructValue(blocks.StructValue):
    @property
    def buttons(self):
        blocks = self.get("button_links", [])
        buttons = []

        for block in blocks:
            label = block.value.get("label")
            link = block.value.get("link")

            if block.block_type == 'internal':
                link_url = link.url
            elif block.block_type == 'external':
                link_url = link
            else:
                link_url = ''

            buttons.append({
                "label": label,
                "link_url": link_url,
            })

        return buttons


class CurrentEventBlock(blocks.StructBlock):
    title = blocks.CharBlock('Heading for the card.')

    link_label = blocks.CharBlock('Label of the link below the heading.')

    link_url = blocks.URLBlock('URL of the link below the heading.')

    image = ImageChooserBlock()

    body = blocks.TextBlock(help_text='Body text of the card.')

    button_links = blocks.StreamBlock(
        [
            ('internal', CurrentEventButtonInternalPage()),
            ('external', CurrentEventButtonExternalPage())
        ],
        max_num=2,
    )

    class Meta:
        value_class = CurrentEventBlockStructValue


class CurrentEventsSliderListBlock(blocks.StructBlock):
    title = blocks.CharBlock()

    current_events = blocks.ListBlock(CurrentEventBlock())

    class Meta:
        icon = 'list-ul'
        help_text = "Recommendation: No more than 5 items should be in this slider."
        template = 'wagtailpages/blocks/current_events_slider_list_block.html'
