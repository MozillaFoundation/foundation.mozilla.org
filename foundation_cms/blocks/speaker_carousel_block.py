from wagtail.blocks import CharBlock, StreamBlock

from foundation_cms.blocks.common.base_carousel_block import (
    BaseCarouselBlock,
    BaseCarouselItemBlock,
)


class SpeakerItemBlock(BaseCarouselItemBlock):
    name = CharBlock(required=True, max_length=120, help_text="Speaker's full name.")
    role = CharBlock(required=False, max_length=120, help_text="Speaker's role or job title.")
    organization = CharBlock(required=False, max_length=120, help_text="Speaker's organization or company.")

    class Meta:
        icon = "user"
        label = "Speaker Item"
        template_name = "speaker_item_block.html"


class SpeakerCarouselBlock(BaseCarouselBlock):
    items = StreamBlock(
        [("speaker_item", SpeakerItemBlock())], max_num=10, help_text="Maximum of 10 speakers per carousel."
    )

    class Meta:
        icon = "group"
        label = "Speaker Carousel"
        template_name = "speaker_carousel_block.html"
