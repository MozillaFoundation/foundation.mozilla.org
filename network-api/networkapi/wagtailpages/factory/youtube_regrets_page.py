from factory import (
    Faker
)
from wagtail.core.models import Page as WagtailPage
from networkapi.wagtailpages.models import YoutubeRegretsPage
from .abstract import CMSPageFactory
from .mini_site_namespace import MiniSiteNamespaceFactory
from networkapi.utility.faker.helpers import (
    reseed,
    get_homepage
)


class YoutubeRegretsPageFactory(CMSPageFactory):
    class Meta:
        model = YoutubeRegretsPage

    title = "YouTube Regrets"

    headline = Faker('text', max_nb_chars=50)

    intro_text = Faker('streamfield', fields=['text', 'text', 'text', 'text', 'text'])

    intro_images = Faker('streamfield', fields=[
      'basic_image', 'basic_image', 'basic_image', 'basic_image', 'basic_image']
    )

    faq = Faker('streamfield', fields=['paragraph'])

    regret_stories = Faker('streamfield', fields=[
      'youtube_story', 'youtube_story', 'youtube_story', 'youtube_story', 'youtube_story']
    )


def generate(seed):
    home_page = get_homepage()
    reseed(seed)

    try:
        campaign_namespace = WagtailPage.objects.get(title='campaigns')
        print('campaigns namespace exists')
    except WagtailPage.DoesNotExist:
        print('Generating a campaigns namespace')
        campaign_namespace = MiniSiteNamespaceFactory.create(
            parent=home_page,
            title='campaigns',
            live=False
        )

    reseed(seed)

    try:
        WagtailPage.objects.get(title='YouTube Regrets')
        print('YouTube Regrets page exists')
    except WagtailPage.DoesNotExist:
        print('Generating a YouTube Regrets page')
        YoutubeRegretsPageFactory.create(parent=campaign_namespace)

    reseed(seed)
