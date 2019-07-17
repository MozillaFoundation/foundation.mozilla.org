import json

from urllib import request, parse
from django.conf import settings
from wagtail.core import blocks

from .annotated_image_block import AnnotatedImageBlock
from .airtable_block import AirTableBlock
from .aligned_image_block import AlignedImageBlock
from .bootstrap_spacer_block import BootstrapSpacerBlock
from .iframe_block import iFrameBlock
from .image_block import ImageBlock
from .image_grid import ImageGrid, ImageGridBlock
from .image_text_block import ImageTextBlock
from .image_text_mini import ImageTextMini
from .link_button_block import LinkButtonBlock
from .pulse_project_list import PulseProjectList
from .quote_block import QuoteBlock
from .video_block import VideoBlock

__all__ = [
    AnnotatedImageBlock,
    AirTableBlock,
    AlignedImageBlock,
    BootstrapSpacerBlock,
    iFrameBlock,
    ImageBlock,
    ImageGrid,
    ImageGridBlock,
    ImageTextBlock,
    ImageTextMini,
    LinkButtonBlock,
    PulseProjectList,
    QuoteBlock,
    VideoBlock,
]


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
