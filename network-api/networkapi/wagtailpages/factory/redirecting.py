from networkapi.wagtailpages.models import RedirectingPage
from wagtail_factories import PageFactory
from wagtail.core.models import Page as WagtailPage

from networkapi.utility.faker.helpers import (
    reseed
)


class RedirectingPageFactory(PageFactory):
    class Meta:
        model = RedirectingPage

    title = 'redirecting to about page'


def generate(seed):
    reseed(seed)

    try:
        WagtailPage.objects.get(title='redirecting to about page')
        print('news page exists')
    except WagtailPage.DoesNotExist:
        print('Generating an empty News Page')
        RedirectingPageFactory.create(URL='/about')
