from networkapi.wagtailpages.models import NewsPage
from wagtail_factories import PageFactory
from wagtail.core.models import Page as WagtailPage

from networkapi.utility.faker.helpers import (
    reseed,
    get_homepage
)


class NewsPageFactory(PageFactory):
    class Meta:
        model = NewsPage

    title = 'news'


def generate(seed):
    home_page = get_homepage()
    reseed(seed)

    try:
        WagtailPage.objects.get(title='news')
        print('news page exists')
    except WagtailPage.DoesNotExist:
        print('Generating an empty News Page')
        NewsPageFactory.create(
            parent=home_page,
            show_in_menus=False
        )
