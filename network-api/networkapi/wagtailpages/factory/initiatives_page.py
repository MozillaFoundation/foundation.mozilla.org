from networkapi.wagtailpages.models import InitiativesPage
from wagtail_factories import PageFactory
from wagtail.core.models import Page as WagtailPage

from networkapi.utility.faker.helpers import (
    reseed,
    get_homepage
)


class InitiativesPageFactory(PageFactory):
    class Meta:
        model = InitiativesPage

    title = 'initiatives'


def generate(seed):
    home_page = get_homepage()
    reseed(seed)

    try:
        WagtailPage.objects.get(title='initiatives')
        print('initiatives page exists')
    except WagtailPage.DoesNotExist:
        print('Generating an empty Initiatives Page')
        InitiativesPageFactory.create(
            parent=home_page,
            show_in_menus=False
        )
