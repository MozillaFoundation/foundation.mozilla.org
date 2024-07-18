from wagtail import blocks

from networkapi.wagtailpages.pagemodels import customblocks


class CarouselTextBlock(blocks.StructBlock):
    heading = blocks.CharBlock(help_text="Heading for the block.", required=False)
    text = blocks.RichTextBlock(features=["bold", "italic", "link"])
    # Use specific link fields for the CTA on the block as opposed to the
    # common.link_blocks.LabelledExternalLinkBlock so it can be marked as
    # required=False.
    link_url = blocks.URLBlock(help_text="A CTA URL for a link displayed", required=False)
    link_label = blocks.CharBlock(help_text="Label for the CTA link.", required=False)
    link = blocks.ListBlock(customblocks.LinkBlock(), min_num=0, max_num=1, help_text="A CTA Link for the carousel")
    carousel_images = blocks.ListBlock(customblocks.ImageBlock(), max_num=4)

    class Meta:
        icon = "placeholder"
        template = "fragments/blocks/carousel_text_block.html"
        label = "Carousel and Text Block"
