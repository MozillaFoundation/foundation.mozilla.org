from networkapi.wagtailpages.models import Styleguide
from wagtail_factories import PageFactory
from wagtail.core.models import Page as WagtailPage
from networkapi.utility.faker.helpers import (
    reseed,
    get_homepage
)


class StyleguideFactory(PageFactory):
    class Meta:
        model = Styleguide

    title = 'style-guide'


def generate(seed):
    home_page = get_homepage()
    reseed(seed)

    try:
        WagtailPage.objects.get(title='style-guide')
        print('styleguide page exists')
    except WagtailPage.DoesNotExist:
        print('Generating a Styleguide Page')
        StyleguideFactory.create(parent=home_page)
