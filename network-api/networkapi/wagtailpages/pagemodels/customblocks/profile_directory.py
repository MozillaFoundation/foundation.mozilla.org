import json
from django.core import serializers
from urllib import request, parse

from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from wagtail.core import blocks
from wagtail.core.blocks.stream_block import StreamBlockValidationError
from wagtail.core.blocks.struct_block import StructBlockValidationError
from wagtail.snippets.blocks import SnippetChooserBlock

from .latest_profile_list import LatestProfileList


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


class TabbedProfileDirectory(blocks.StructBlock):
    """
    This component is set up to create a directory with tabs. The tabs are filtered on a
    specific profile field (e.g. profile_type).
    https://github.com/mozilla/foundation.mozilla.org/issues/7422
    """
    tabs = SnippetChooserBlock(
        'wagtailpages.PulseFilter',
        help_text=(
            'The profile information to create tabs on. The first option in the snippet'
            ' will be used as the initial filter.'
        ),
    )
    subfilters = blocks.StreamBlock(
        [
            ('filter', SnippetChooserBlock('wagtailpages.PulseFilter')),
        ],
        max_num=1,
        required=False,
    )

    advanced_filter_header = blocks.StaticBlock(
        label='-------- ADVANCED FILTERS: OPTIONS TO DISPLAY FEWER, MORE TARGETED RESULTS. --------',
        admin_text=(
            'Note that the filter not be used if selected as the tabs filter or as one of the subfilters.'
            ' For example, if the tabs filter profile types, the profile type field below will be ignored.'
        ),
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

    class Meta:
        template = 'wagtailpages/blocks/tabbed_profile_directory.html'
        icon = 'group'

    def clean(self, value):
        result = super().clean(value)
        errors = {}

        # Check if any of the subfilter snippets are the same as the tabs snippet.
        for index, subfilter_block in enumerate(value['subfilters']):
            if subfilter_block.value.pk == value['tabs'].pk:
                errors['subfilters'] = ErrorList([
                    StreamBlockValidationError(
                        block_errors={
                            index: ErrorList(
                                [
                                    ValidationError(ErrorList(['The subfilter cannot be the same as the tabs.'])),
                                ]
                            )
                        },
                        non_block_errors=ErrorList(),
                    )
                ])

        if errors:
            raise StructBlockValidationError(errors)

        return result

    def get_context(self, value, parent_context=None, ordering=False):
        context = super().get_context(value, parent_context=parent_context)
        pulse_api = settings.FRONTEND['PULSE_API_DOMAIN']

        query_args = {
            'profile_type': value['profile_type'],
            'program_type': value['program_type'],
            'program_year': value['year'],
            'ordering': ordering if ordering else 'custom_name',
            'is_active': 'true',
            'format': 'json',
        }

        # Use first tabs filter option as the initial filter.
        tabs = value['tabs']
        query_args[tabs.filter_key] = tabs.options.first().filter_value

        # Remove specific filter if the filter is in use for subfilters.
        for subfilter_block in value['subfilters']:
            filter_key = subfilter_block.value.filter_key
            if filter_key in query_args:
                query_args.pop(filter_key)

        # Filter out emptish values
        query_args = {k: v for k, v in query_args.items() if v}

        url = '{pulse_api}/api/pulse/v2/profiles/?{query}'.format(
            pulse_api=pulse_api,
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
        context['api_endpoint'] = f"{pulse_api}/api/pulse/v2/profiles/?ordering=custom_name&is_active=true&format=json"
        context['tab_options'] = serializers.serialize('json', value['tabs'].options.all())

        return context
