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
from .latest_profile_list import LatestProfileList
from .link_button_block import LinkButtonBlock
from .profile_by_id import ProfileById
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
    LatestProfileList,
    LinkButtonBlock,
    ProfileById,
    PulseProjectList,
    QuoteBlock,
    VideoBlock,
]


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
