from factory import Faker, SubFactory
from wagtail.models import Page as WagtailPage
from wagtail_factories import PageFactory

from networkapi.utility.faker.helpers import get_homepage, reseed
from networkapi.wagtailpages.factory import image_factory
from networkapi.wagtailpages.models import (
    AppInstallPage,
    YoutubeRegrets2021Page,
    YoutubeRegrets2022Page,
    YoutubeRegretsPage,
    YoutubeRegretsReporterPage,
)

from .bannered_campaign_page import BanneredCampaignPageFactory
from .campaign_page import CampaignIndexPageFactory
from .petition import PetitionFactory


class YoutubeRegretsPageFactory(PageFactory):
    class Meta:
        model = YoutubeRegretsPage
        exclude = (
            "title_text",
            "header_text",
            "header",
        )

    title = "YouTube Regrets"
    headline = Faker("text", max_nb_chars=50)
    intro_text = Faker("streamfield", fields=["text"] * 5)
    intro_images = Faker("streamfield", fields=["basic_image"] * 10)
    faq = Faker("streamfield", fields=["paragraph"])
    regret_stories = Faker("streamfield", fields=["regret_story"] * 28)


class AppInstallPageFactory(PageFactory):
    class Meta:
        model = AppInstallPage
        exclude = (
            "title_text",
            "header_text",
            "header",
        )

    title = "Regrets Reporter Page"
    slug = "regretsreporter"
    hero_heading = Faker("text", max_nb_chars=50)
    hero_subheading = Faker("text", max_nb_chars=50)
    hero_background = SubFactory(image_factory.ImageFactory)
    hero_video = Faker("url")
    cta = SubFactory(PetitionFactory)
    body = Faker("streamfield", fields=["header", "paragraph", "image", "spacer", "image_text", "quote"])


class YoutubeRegrets2021PageFactory(PageFactory):
    class Meta:
        model = YoutubeRegrets2021Page
        exclude = (
            "title_text",
            "header_text",
            "header",
        )

    title = "YouTube Regrets 2021"
    slug = "findings"


class YoutubeRegrets2022PageFactory(PageFactory):
    class Meta:
        model = YoutubeRegrets2022Page
        exclude = (
            "title_text",
            "header_text",
            "header",
        )

    title = "YouTube Regrets 2022"
    slug = "findings-2022"


class YoutubeRegretsReporterPageFactory(PageFactory):
    class Meta:
        model = YoutubeRegretsReporterPage
        exclude = (
            "title_text",
            "header_text",
            "header",
        )

    title = "YouTube Regrets"
    headline = Faker("text", max_nb_chars=50)
    intro_text = Faker("streamfield", fields=["text"] * 5)
    intro_images = Faker("streamfield", fields=["basic_image"] * 10)


def generate(seed):
    home_page = get_homepage()
    reseed(seed)

    try:
        campaign_index_page = WagtailPage.objects.get(title="campaigns")
        print("campaign index page exists")
    except WagtailPage.DoesNotExist:
        print("Generating a campaign index page")
        campaign_index_page = CampaignIndexPageFactory.create(parent=home_page, title="campaigns", live=True)

    reseed(seed)

    title = "YouTube Regrets"

    try:
        YoutubeRegretsPage.objects.get(title=title)
        print("YouTube Regrets page exists")
    except YoutubeRegretsPage.DoesNotExist:
        print("Generating YouTube Regrets Page under campaigns namespace")
        YoutubeRegretsPageFactory.create(parent=campaign_index_page, title=title)

    reseed(seed)

    reporter_page_title = "Regrets Reporter"

    try:
        YoutubeRegretsReporterPage.objects.get(title=reporter_page_title)
        print("Regrets Reporter page exists")
    except YoutubeRegretsReporterPage.DoesNotExist:
        print("Generating Regrets Reporter Page under campaigns namespace")
        youtube_regrets = YoutubeRegretsReporterPageFactory.create(
            parent=campaign_index_page,
            title=reporter_page_title,
        )
        YoutubeRegrets2021PageFactory.create(parent=youtube_regrets)
        YoutubeRegrets2022PageFactory.create(parent=youtube_regrets)
    reseed(seed)

    # App Install Page
    # Checking for a bannered campaign page titled "Youtube Regrets", and then creating the landing page if
    # it does not exist.
    try:
        youtube_bannered_campaign_page = WagtailPage.objects.child_of(home_page).get(title=title)
        print("Youtube Regrets Bannered Campaign Page exists")
        # If extension landing page does not exist, create it.
        if not WagtailPage.objects.child_of(youtube_bannered_campaign_page).type(AppInstallPage):
            print("Generating App Install Page")
            AppInstallPageFactory.create(parent=youtube_bannered_campaign_page)

    # If bannered "YouTube Regrets" campaign page does not exist, create it and the extension landing page.
    except WagtailPage.DoesNotExist:
        print("Generating a Youtube Bannered Campaign Page and App Install Page")
        youtube_bannered_campaign_page = BanneredCampaignPageFactory.create(
            parent=home_page,
            title="YouTube Regrets",
            slug="youtube",
            show_in_menus=False,
            live=True,
        )
        AppInstallPageFactory.create(parent=youtube_bannered_campaign_page)

    reseed(seed)
