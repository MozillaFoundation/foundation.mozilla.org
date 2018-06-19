import re

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
        if self['outline'] is True and 'ghost' not in btn_class:
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
            ('btn-danger', 'Danger button'),
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
        template = 'wagtailpages/blocks/link_button_block.html'
        value_class = LinkButtonValue


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    altText = blocks.CharBlock(
        required=True,
        help_text='Image description (for screen readers).'
    )

    class Meta:
        icon = 'image'
        template = 'wagtailpages/blocks/image_block.html'


class AnnotatedImageBlock(ImageBlock):
    caption = blocks.CharBlock(
        required=False
    )
    captionURL = blocks.CharBlock(
        required=False,
        help_text='Optional URL that this caption should link out to.'
    )

    class Meta:
        icon = 'image'
        template = 'wagtailpages/blocks/annotated_image_block.html'
        help_text = 'Design Guideline: Please crop images to a 16:6 aspect ratio when possible.'


class AlignedImageBlock(ImageBlock):
    alignment = blocks.ChoiceBlock(
        choices=[
            ('', 'Do not apply any explicit alignment classes.'),
            ('left-align', 'Left-align this image with the page content.'),
            ('right-align', 'Right-align this image with the page content.'),
            ('center', 'Center this image with the page content.'),
            ('full-width', 'Make this image full-width.'),
        ],
        default='',
        required=False
    )

    class Meta:
        icon = 'image'
        template = 'wagtailpages/blocks/aligned_image_block.html'


class ImageTextBlock(blocks.StructBlock):
    text = blocks.RichTextBlock(
        features=['bold', 'italic', 'link', ]
    )
    image = ImageBlock()
    ordering = blocks.ChoiceBlock(
        choices=[
            ('left', 'Image on the left'),
            ('right', 'Image on the right'),
        ],
        default='left',
    )

    class Meta:
        icon = 'doc-full'
        template = 'wagtailpages/blocks/image_text_block.html'
        group = 'Deprecated'


class ImageTextBlock2(ImageBlock):
    text = blocks.RichTextBlock(
        features=['link', 'h2', 'h3', 'h4', 'h5', 'h6']
    )
    url = blocks.CharBlock(
        required=False,
        help_text='Optional URL that this image should link out to.',
    )
    small = blocks.BooleanBlock(
        required=False,
        help_text='Use smaller, fixed image size (eg: icon)',
    )

    class Meta:
        icon = 'doc-full'
        template = 'wagtailpages/blocks/image_text_block2.html'


class FigureBlock(blocks.StructBlock):
    figure = AlignedImageBlock()
    caption = blocks.CharBlock(
        required=False,
        help_text='Please remember to properly attribute any images we use.'
    )
    url = blocks.CharBlock(
        required=False,
        help_text='Optional URL that this figure should link out to.',
    )

    class Meta:
        icon = 'picture'
        template = 'wagtailpages/blocks/figure_block.html'
        group = 'Deprecated'


class FigureBlock2(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(
        required=False,
        help_text='Please remember to properly attribute any images we use.'
    )
    url = blocks.CharBlock(
        required=False,
        help_text='Optional URL that this figure should link out to.',
    )


class FigureGridBlock(blocks.StructBlock):
    grid_items = blocks.ListBlock(FigureBlock())

    class Meta:
        # this is probably the wrong icon but let's run with it for now
        icon = 'grip'
        template = 'wagtailpages/blocks/figure_grid_block.html'
        group = 'Deprecated'


class FigureGridBlock2(blocks.StructBlock):
    grid_items = blocks.ListBlock(FigureBlock2())

    class Meta:
        # this is probably the wrong icon but let's run with it for now
        icon = 'grip'
        template = 'wagtailpages/blocks/figure_grid_block2.html'


class BootstrapSpacerBlock(blocks.StructBlock):
    """
    See https://getbootstrap.com/docs/4.0/utilities/spacing/
    """

    # property = blocks.ChoiceBlock(
    #    choices=[
    #        ('m', 'Margin'),
    #        #('p', 'Padding'),
    #    ],
    #    default='m',
    # )

    # sides = blocks.ChoiceBlock(
    #    choices=[
    #        ('t', 'top'),
    #        ('b', 'bottom'),
    #        ('l', 'left'),
    #        ('r', 'right'),
    #        ('x', 'left + right'),
    #        ('y', 'top+bottom'),
    #        ('', 'all sides'),
    #    ],
    #    default='',
    # )

    size = blocks.ChoiceBlock(
        choices=[
            # ('0', 'no spacing'),
            ('1', 'quarter spacing'),
            ('2', 'half spacing'),
            ('3', 'single spacing'),
            ('4', 'one and a half spacing'),
            ('5', 'triple spacing'),
            # ('auto', 'automagical'),
        ],
        default='3',
    )

    class Meta:
        icon = 'arrows-up-down'
        template = 'wagtailpages/blocks/bootstrap_spacer_block.html'
        help_text = 'A bootstrap based vertical spacing block.'


class iFrameBlock(blocks.StructBlock):
    url = blocks.CharBlock(
        help_text='Please note that only URLs from white-listed domains will work.'
    )
    caption = blocks.CharBlock(
        required=False
    )
    captionURL = blocks.CharBlock(
        required=False,
        help_text='Optional URL that this caption should link out to.'
    )

    class Meta:
        template = 'wagtailpages/blocks/iframe_block.html'


class VideoBlock(blocks.StructBlock):
    url = blocks.CharBlock(
        help_text='Please make sure this is a proper embed URL, or your video will not show up on the page.'
    )
    caption = blocks.CharBlock(
        required=False,
    )
    captionURL = blocks.CharBlock(
        required=False,
        help_text='Optional URL for caption to link to.'
    )

    class Meta:
        template = 'wagtailpages/blocks/video_block.html'


class QuoteBlock(blocks.StructBlock):

    # The goal is to be able to cycle through multiple quotes,
    # so let's accept multiple quotes to start even if we only show one for now.
    # This way we don't have to migrate the model again later

    quotes = blocks.ListBlock(blocks.StructBlock([
        ('quote', blocks.CharBlock()),
        ('attribution', blocks.CharBlock())
    ]))

    class Meta:
        template = 'wagtailpages/blocks/quote_block.html'
        icon = 'openquote'
        help_text = 'Multiple quotes can be entered, but for now we are only using the first'


class PulseProjectQueryValue(blocks.StructValue):
    @property
    def query(self):
        # Replace any combination of spaces and commas with a single +
        # because despite instructions to use spaces, someone, at some
        # point, will accidentally use a comma, and that should be fine.
        search_terms = self['search_terms'].strip()
        query = re.sub(r'[\s,]+', '+', search_terms)
        return query

    @property
    def size(self):
        max_number_of_results = self['max_number_of_results']
        return '' if max_number_of_results <= 0 else max_number_of_results

    @property
    def rev(self):
        # The default API behaviour is newest-first, so the "rev" attribute
        # should only have an attribute value when oldest-first is needed.
        newest_first = self['newest_first']
        return True if newest_first else ''


class PulseProjectList(blocks.StructBlock):
    search_terms = blocks.CharBlock(
        help_text='Fill in any number of pulse entry search terms (separated by spaces).',
    )

    max_number_of_results = blocks.IntegerBlock(
        min_value=0,
        default=0,
        required=False,
        help_text='The maximum number of results to fetch (use 0 for default maximum of 48)',
    )

    newest_first = blocks.BooleanBlock(
        default=True,
        help_text='Check this box to list entries "newest first".',
        required=False,
    )

    only_featured_entries = blocks.BooleanBlock(
        default=False,
        help_text='Check this box to only get results from the featured entry list.',
        required=False,
    )

    class Meta:
        template = 'wagtailpages/blocks/pulse_project_list.html'
        icon = 'site'
        value_class = PulseProjectQueryValue
