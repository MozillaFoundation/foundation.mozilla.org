from wagtail import blocks

from foundation_cms.legacy_apps.wagtailpages.pagemodels import customblocks


class CarouselTextBlock(blocks.StructBlock):
    heading = blocks.CharBlock(help_text="Heading for the block.", required=False)
    text = blocks.RichTextBlock(features=["bold", "italic", "link"])
    link = blocks.ListBlock(customblocks.LinkBlock(), min_num=0, max_num=1, help_text="A CTA Link for the carousel")
    carousel_images = blocks.ListBlock(customblocks.ImageBlock(), max_num=4)

    class Meta:
        icon = "placeholder"
        template = "fragments/blocks/carousel_text_block.html"
        label = "Carousel and Text Block"
