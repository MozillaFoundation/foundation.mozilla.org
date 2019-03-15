import json

from urllib import request, parse
from django.conf import settings
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


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
            ('btn-normal', 'Normal button'),
            ('btn-ghost', 'Ghost button'),
        ],
        default='btn-normal',
    )

    class Meta:
        icon = 'link'
        template = 'wagtailpages/blocks/link_button_block.html'


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    altText = blocks.CharBlock(
        required=True,
        help_text='Image description (for screen readers).'
    )

    class Meta:
        icon = 'image'
        template = 'wagtailpages/blocks/image_block.html'


class AirTableBlock(blocks.StructBlock):
    url = blocks.URLBlock(
        help_text="Copied from the Airtable embed code. The word 'embed' will be in the url"
    )
    height = blocks.IntegerBlock(
        default=533,
        help_text="The height of the view on a desktop, usually copied from the Airtable embed code",
    )

    class Meta:
        icon = 'placeholder'
        template = 'wagtailpages/blocks/airtable_block.html'


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


class ImageTextBlock2(ImageBlock):
    text = blocks.RichTextBlock(
        features=['bold', 'italic', 'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'link']
    )
    url = blocks.CharBlock(
        required=False,
        help_text='Optional URL that this image should link out to.',
    )
    small = blocks.BooleanBlock(
        required=False,
        help_text='Use smaller, fixed image size (eg: icon)',
    )
    top_divider = blocks.BooleanBlock(
        required=False,
        help_text='Optional divider above content block.',
    )
    bottom_divider = blocks.BooleanBlock(
        required=False,
        help_text='Optional divider below content block.',
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        divider_styles = []
        if value.get("top_divider"):
            divider_styles.append('div-top')
        if value.get("bottom_divider"):
            divider_styles.append('div-bottom')
        context['divider_styles'] = ' '.join(divider_styles)
        return context

    class Meta:
        icon = 'doc-full'
        template = 'wagtailpages/blocks/image_text_block2.html'


class ImageTextMini(ImageBlock):
    text = blocks.RichTextBlock(
        features=['bold', 'italic', 'link']
    )

    class Meta:
        icon = 'doc-full'
        template = 'wagtailpages/blocks/image_text_mini.html'


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
        help_text='Test your search at mozillapulse.org/search',
        label='Search',
        required=False,
    )

    max_number_of_results = blocks.IntegerBlock(
        min_value=0,
        max_value=12,
        default=6,
        required=True,
        help_text='Choose 1-12. If you want visitors to see more, link to a search or tag on Pulse.',
    )

    only_featured_entries = blocks.BooleanBlock(
        default=False,
        label='Display only featured entries',
        help_text='Featured items are selected by Pulse moderators.',
        required=False,
    )

    newest_first = blocks.ChoiceBlock(
        choices=[
            ('True', 'Show newer entries first'),
            ('False', 'Show older entries first'),
        ],
        required=True,
        label='Sort',
        default='True',
    )

    advanced_filter_header = blocks.StaticBlock(
        label=' ',
        admin_text='-------- ADVANCED FILTERS: OPTIONS TO DISPLAY FEWER, MORE TARGETED RESULTS. --------',
    )

    issues = blocks.ChoiceBlock(
        choices=[
            ('all', 'All'),
            ('Decentralization', 'Decentralization'),
            ('Digital Inclusion', 'Digital Inclusion'),
            ('Online Privacy & Security', 'Online Privacy & Security'),
            ('Open Innovation', 'Open Innovation'),
            ('Web Literacy', 'Web Literacy'),
        ],
        required=True,
        default='all'
    )

    help = blocks.ChoiceBlock(
        choices=[
            ('all', 'All'),
            ('Attend', 'Attend'),
            ('Create content', 'Create content'),
            ('Code', 'Code'),
            ('Design', 'Design'),
            ('Fundraise', 'Fundraise'),
            ('Join community', 'Join community'),
            ('Localize & translate', 'Localize & translate'),
            ('Mentor', 'Mentor'),
            ('Plan & organize', 'Plan & organize'),
            ('Promote', 'Promote'),
            ('Take action', 'Take action'),
            ('Test & feedback', 'Test & feedback'),
            ('Write documentation', 'Write documentation'),
        ],
        required=True,
        default='all',
        label='Type of help needed',
    )

    class Meta:
        template = 'wagtailpages/blocks/pulse_project_list.html'
        icon = 'site'
        value_class = PulseProjectQueryValue


class ProfileById(blocks.StructBlock):

    ids = blocks.CharBlock(
        label='Profile by ID',
        help_text='Show profiles for pulse users with specific profile ids'
                  ' (mozillapulse.org/profile/[##]). For multiple profiles'
                  ', specify a comma separated list (e.g. 85,105,332).'
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        ids = context['block'].value['ids']
        data = list()

        # FIXME: the protocol should be part of the pulse api variable.
        #   see: https://github.com/mozilla/foundation.mozilla.org/issues/1824

        url = "{pulse_api}/api/pulse/v2/profiles/?format=json&ids={ids}".format(
            pulse_api=settings.FRONTEND['PULSE_API_DOMAIN'],
            ids=ids
        )

        try:
            response = request.urlopen(url)
            response_data = response.read()
            data = json.loads(response_data)

        except (IOError, ValueError) as exception:
            print(str(exception))
            pass

        context['profiles'] = data
        return context

    class Meta:
        template = 'wagtailpages/blocks/profile_blocks.html'
        icon = 'user'


class LatestProfileQueryValue(blocks.StructValue):
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


class LatestProfileList(blocks.StructBlock):
    max_number_of_results = blocks.IntegerBlock(
        min_value=1,
        max_value=48,
        default=12,
        required=True,
        help_text='Pick up to 48 profiles.',
    )

    advanced_filter_header = blocks.StaticBlock(
        label=' ',
        admin_text='-------- ADVANCED FILTERS: OPTIONS TO DISPLAY FEWER, MORE TARGETED RESULTS. --------',
    )

    profile_type = blocks.CharBlock(
        required=False,
        default='',
        help_text='Example: Fellow.'
    )

    program_type = blocks.CharBlock(
        required=False,
        default='',
        help_text='Example: Tech Policy.'
    )

    year = blocks.CharBlock(
        required=False,
        default=''
    )

    def get_context(self, value, parent_context=None, no_limit=False, initial_year=False, ordering=False):
        context = super().get_context(value, parent_context=parent_context)

        query_args = {
            'limit': value['max_number_of_results'],
            'profile_type': value['profile_type'],
            'program_type': value['program_type'],
            'program_year': initial_year if initial_year else value['year'],
            'ordering': ordering if ordering else '-id',
            'is_active': 'true',
            'format': 'json',
        }

        # Removing after the fact is actually easier than
        # conditionally adding and then filtering the list.
        if no_limit:
            query_args.pop('limit')

        # Filter out emptish values
        query_args = {k: v for k, v in query_args.items() if v}

        url = "{pulse_api}/api/pulse/v2/profiles/?{query}".format(
            pulse_api=settings.FRONTEND['PULSE_API_DOMAIN'],
            query=parse.urlencode(query_args)
        )

        data = []

        try:
            response = request.urlopen(url)
            response_data = response.read()
            data = json.loads(response_data)

            for profile in data:
                profile['created_entries'] = False
                profile['published_entries'] = False
                profile['entry_count'] = False
                profile['user_bio_long'] = False

        except (IOError, ValueError) as exception:
            print(str(exception))
            pass

        context['profiles'] = data
        context['profile_type'] = value['profile_type']
        context['program_type'] = value['program_type']
        context['program_year'] = value['year']

        return context

    class Meta:
        template = 'wagtailpages/blocks/profile_blocks.html'
        icon = 'group'
        value_class = LatestProfileQueryValue


class ProfileDirectory(LatestProfileList):
    """
    NOTE:
    this component has been set up specifically for year
    filtering for its initial pass. It does not do any
    kind of filter detection and query argument juggling
    yet, which is why the default filter_values text is
    literally the string that matches the filter that
    was used on the fellowship directory page prior to
    porting to the CMS.
    There is an issue open to make this component more
    generic. See:
    https://github.com/mozilla/foundation.mozilla.org/issues/2700
    """

    filter_values = blocks.CharBlock(
        required=True,
        default='2019,2018,2017,2016,2015,2014,2013',
        help_text='Example: 2019,2018,2017,2016,2015,2014,2013'
    )

    def get_context(self, value, parent_context=None):
        pulse_api = settings.FRONTEND['PULSE_API_DOMAIN']
        filter_values = value['filter_values']
        years = filter_values.split(",")
        initial_year = years[0]

        context = super().get_context(
            value,
            parent_context=parent_context,
            no_limit=True,
            initial_year=initial_year,
            ordering='custom_name'
        )

        context['filters'] = years
        context['api_endpoint'] = f"{pulse_api}/api/pulse/v2/profiles/?ordering=custom_name&is_active=true&format=json"
        return context

    class Meta:
        template = 'wagtailpages/blocks/profile_directory.html'
        icon = 'group'
