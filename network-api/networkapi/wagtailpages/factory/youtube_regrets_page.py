from factory import (
    Faker
)
from wagtail.core.models import Page as WagtailPage
from networkapi.wagtailpages.models import (
    YoutubeRegretsPage,
    YoutubeRegretsReporterPage,
    YoutubeRegretsReporterExtensionPage,
    YoutubeRegrets2021Page,
)
from wagtail_factories import (
    PageFactory
)
from .campaign_page import CampaignIndexPageFactory
from .bannered_campaign_page import BanneredCampaignPageFactory
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


class YoutubeRegretsReporterExtensionPageFactory(PageFactory):
    class Meta:
        model = YoutubeRegretsReporterExtensionPage
        exclude = (
            'title_text',
            'header_text',
            'header',
        )

    title = 'Regrets Reporter Extension'
    slug = 'regretsreporter'


class YoutubeRegrets2021PageFactory(PageFactory):
    class Meta:
        model = YoutubeRegrets2021Page
        exclude = (
            'title_text',
            'header_text',
            'header',
        )

    title = 'YouTube Regrets 2021'
    slug = 'findings'


class YoutubeRegretsReporterPageFactory(PageFactory):
    class Meta:
        model = YoutubeRegretsReporterPage
        exclude = (
            'title_text',
            'header_text',
            'header',
        )

    title = 'YouTube Regrets'
    headline = Faker('text', max_nb_chars=50)
    intro_text = Faker('streamfield', fields=['text']*5)
    intro_images = Faker('streamfield', fields=['basic_image']*10)


def generate(seed):
    home_page = get_homepage()
    reseed(seed)

    try:
        campaign_index_page = WagtailPage.objects.get(title='campaigns')
        print('campaign index page exists')
    except WagtailPage.DoesNotExist:
        print('Generating a campaign index page')
        campaign_index_page = CampaignIndexPageFactory.create(
            parent=home_page,
            title='campaigns',
            live=True
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

    reporter_page_title = 'Regrets Reporter'

    try:
        YoutubeRegretsReporterPage.objects.get(title=reporter_page_title)
        print('Regrets Reporter page exists')
    except YoutubeRegretsReporterPage.DoesNotExist:
        print('Generating Regrets Reporter Page under campaigns namespace')
        youtube_regrets = YoutubeRegretsReporterPageFactory.create(
            parent=campaign_index_page,
            title=reporter_page_title,
        )
        YoutubeRegrets2021PageFactory.create(parent=youtube_regrets)
    reseed(seed)

    # Youtube Extension Landing page
    # Checking for a bannered campaign page titled "Youtube Regrets", and then creating the landing page if
    # it does not exist.
    try:
        youtube_bannered_campaign_page = WagtailPage.objects.child_of(home_page).get(title=title)
        print('Youtube Regrets bannered campaign page exists')
        # If extension landing page does not exist, create it.
        if not WagtailPage.objects.child_of(youtube_bannered_campaign_page).type(YoutubeRegretsReporterExtensionPage):
            print("Generating extension landing page")
            YoutubeRegretsReporterExtensionPageFactory.create(parent=youtube_bannered_campaign_page)

    # If bannered "YouTube Regrets" campaign page does not exist, create it and the extension landing page.
    except WagtailPage.DoesNotExist:
        print('Generating a youtube bannered campaign page and extension landing page')
        youtube_bannered_campaign_page = BanneredCampaignPageFactory.create(
            parent=home_page,
            title='YouTube Regrets',
            live=True
        )
        YoutubeRegretsReporterExtensionPageFactory.create(parent=youtube_bannered_campaign_page)

    reseed(seed)
