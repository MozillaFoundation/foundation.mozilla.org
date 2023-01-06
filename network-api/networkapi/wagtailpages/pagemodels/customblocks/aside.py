from wagtail import blocks


class AsideContentBlock(blocks.StructBlock):
    class Meta:
        icon = "placeholder"
        template = "wagtailpages/blocks/aside_content.html"

    title = blocks.CharBlock(help_text="Heading for the card.", required=False)

    body = blocks.TextBlock(help_text="Body text of the card.", required=False)
