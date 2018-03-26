from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class LinkButtonValue(blocks.StructValue):
    # and https://stackoverflow.com/questions/49374083
    # see http://docs.wagtail.io/en/v2.0/topics/streamfield.html#custom-value-class-for-structblock

    @property
    def css(self):
        # Note that StructValue is a dict-like object, so `styling` and `outline`
        # need to be accessed as dictionary keys
        btn_class = self['styling']
        if self['outline'] is True:
            btn_class = btn_class.replace('btn-', 'btn-outline-')
        return btn_class


class LinkButtonBlock(blocks.StructBlock):
    label = blocks.CharBlock()

    # We use a char block because UrlBlock does not
    # allow for relative linking.
    URL = blocks.CharBlock()

    # Buttons can have different looks, so we
    # offer the choice to decide which styling
    # should be used.
    styling = blocks.ChoiceBlock(
        choices=[
            ('btn-primary', 'Primary button'),
            ('btn-secondary', 'Secondary button'),
            ('btn-success', 'Success button'),
            ('btn-info', 'Info button'),
            ('btn-warning', 'Warning button'),
            ('btn-error', 'Error button'),
            ('btn-ghost', 'Ghost button'),
        ],
        default='btn-info',
    )

    outline = blocks.BooleanBlock(
        default=False,
        required=False
    )

    class Meta:
        icon = 'link'
        template = 'minisites/blocks/link_button_block.html'
        value_class = LinkButtonValue


class ImageTextBlock(blocks.StructBlock):
    text = blocks.CharBlock()
    image = ImageChooserBlock()
    ordering = blocks.ChoiceBlock(
        choices=[
            ('left', 'Image on the left'),
            ('right', 'Image on the right'),
        ],
        default='left',
    )

    class Meta:
        icon = 'doc-full'
        template = 'minisites/blocks/image_text_block.html'


class VerticalSpacerBlock(blocks.StructBlock):
    rem = blocks.IntegerBlock()

    class Meta:
        icon = 'arrows-up-down'
        template = 'minisites/blocks/vertical_spacer_block.html'
        help_text = 'the number of "rem" worth of vertical spacing'


class iFrameBlock(blocks.StructBlock):
    url = blocks.CharBlock(
        help_text='Please note that only URLs from white-listed domains will work.'
    )
    height = blocks.IntegerBlock(default=450)

    class Meta:
        template = 'minisites/blocks/iframe_block.html'


class VideoBlock(blocks.StructBlock):
    url = blocks.CharBlock(
        help_text='Please make sure this is a proper embed URL, or your video will not show up on the page.'
    )
    height = blocks.IntegerBlock(default=450)

    class Meta:
        template = 'minisites/blocks/video_block.html'
