from factory import (
    Faker
)
from wagtail.core.models import Page as WagtailPage
from networkapi.wagtailpages.models import YoutubeRegretsPage
from wagtail_factories import (
    PageFactory
)
from .mini_site_namespace import MiniSiteNamespaceFactory
from networkapi.utility.faker.helpers import (
    reseed,
    get_homepage
)


class YoutubeRegretsPageFactory(PageFactory):
    class Meta:
        model = YoutubeRegretsPage
        exclude = (
            'title_text',
            'header_text',
            'header',
        )

    title = 'YouTube Regrets'
    headline = Faker('text', max_nb_chars=50)
    intro_text = Faker('streamfield', fields=['text']*5)
    intro_images = Faker('streamfield', fields=['basic_image']*10)
    faq = Faker('streamfield', fields=['paragraph'])
    regret_stories = Faker('streamfield', fields=['regret_story']*28)


def generate(seed):
    home_page = get_homepage()
    reseed(seed)

    try:
        campaign_index_page = WagtailPage.objects.get(title='campaigns')
        print('campaign index page exists')
    except WagtailPage.DoesNotExist:
        print('Generating a campaign index page')
        campaign_index_page = MiniSiteNamespaceFactory.create(
            parent=home_page,
            title='campaigns',
            live=False
        )

    reseed(seed)

    title = 'YouTube Regrets'

    try:
        YoutubeRegretsPage.objects.get(title=title)
        print('YouTube Regrets page exists')
    except YoutubeRegretsPage.DoesNotExist:
        print('Generating YouTube Regrets Page under campaigns namespace')
        YoutubeRegretsPageFactory.create(parent=campaign_index_page, title=title)

    reseed(seed)
