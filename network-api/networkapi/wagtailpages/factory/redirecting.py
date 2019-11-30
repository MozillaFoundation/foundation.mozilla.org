from networkapi.wagtailpages.models import RedirectingPage
from wagtail_factories import PageFactory
from wagtail.core.models import Page as WagtailPage

from networkapi.utility.faker.helpers import (
    reseed,
    get_homepage
)


class RedirectingPageFactory(PageFactory):
    class Meta:
        model = RedirectingPage

    title = 'redirecting to about page'


def generate(seed):
    home_page = get_homepage()
    reseed(seed)

    try:
        WagtailPage.objects.get(title='redirecting to about page')
        print('Redirecting page exists')
    except WagtailPage.DoesNotExist:
        print('Generating a new Redirecting Page')
        RedirectingPageFactory.create(parent=home_page, URL='/about')
