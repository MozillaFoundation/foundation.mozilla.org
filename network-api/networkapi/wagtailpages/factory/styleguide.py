from networkapi.wagtailpages.models import Styleguide
from wagtail_factories import PageFactory
from wagtail.core.models import Page as WagtailPage
from networkapi.utility.faker.helpers import (
    reseed,
    get_homepage
)

from factory import (
    Faker
)

styleguide_streamfield_fields = [
    'paragraph',
    'image',
    'image_text',
    'image_text_mini',
    'image_grid',
    'video',
    'linkbutton',
    'spacer',
    'quote',
    'double_image',
    'text',
    'full_width_image',
    'card_grid',
    'pulse_listing',
    'profile_listing',
    'recent_blog_entries',
    'blog_set',
    'airtable',
    'typeform',
    'datawrapper'
]


class StyleguideFactory(PageFactory):
    class Meta:
        model = Styleguide

    title = 'Style-guide'
    body = Faker('streamfield', fields=styleguide_streamfield_fields)


def generate(seed):
    home_page = get_homepage()
    reseed(seed)

    try:
        WagtailPage.objects.get(title='Style-guide')
        print('styleguide page exists')
    except WagtailPage.DoesNotExist:
        print('Generating a Styleguide Page')
        StyleguideFactory.create(
            parent=home_page,
            show_in_menus=True
        )
