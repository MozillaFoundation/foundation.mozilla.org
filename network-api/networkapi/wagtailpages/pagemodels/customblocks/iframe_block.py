from wagtail.core import blocks


class iFrameBlock(blocks.StructBlock):
    url = blocks.CharBlock(
        help_text='Please note that only URLs from white-listed domains will work.'
    )
    height = blocks.IntegerBlock(
        required=False,
        help_text='Optional integer pixel value for custom iFrame height'
    )
    caption = blocks.CharBlock(
        required=False
    )
    captionURL = blocks.CharBlock(
        required=False,
        help_text='Optional URL that this caption should link out to.'
    )
    wide_iframe = blocks.BooleanBlock(
        required=False,
        help_text='Check this box for a wider iframe',
    )

    class Meta:
        template = 'wagtailpages/blocks/iframe_block.html'
