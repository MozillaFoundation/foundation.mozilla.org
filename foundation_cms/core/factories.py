import factory
from django.conf import settings
from wagtail.images.models import Image
from wagtail.models import Page, Site
from wagtail_factories import ImageFactory, PageFactory

from .models import HomePage

if settings.HEROKU_APP_NAME:
    REVIEW_APP_NAME = settings.HEROKU_APP_NAME
    REVIEW_APP_HOSTNAME = f"{REVIEW_APP_NAME}.herokuapp.com"


class HomePageFactory(PageFactory):
    class Meta:
        model = HomePage

    title = factory.Faker("sentence", nb_words=4)


# Helper function to handle image setup
class WagtailImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    file = factory.django.ImageField(color="blue")


def create_homepage():
    """
    Create a HomePage
    """

    # Get the site root
    site_root = Page.objects.get(id=1)

    # Create the HomePage page and attach them to the site root
    home_page = HomePageFactory.create(parent=site_root)

    try:
        default_site = Site.objects.get(is_default_site=True)
        default_site.root_page = home_page
        if settings.HEROKU_APP_NAME:
            hostname = REVIEW_APP_HOSTNAME
            port = 80
        else:
            hostname = "localhost"
            port = 8000
        default_site.hostname = hostname
        default_site.port = port
        default_site.site_name = "Foundation Home Page"
        default_site.save()
        print("Updated the default Site")
    except Site.DoesNotExist:
        print("Generating a default Site")
        if settings.HEROKU_APP_NAME:
            hostname = REVIEW_APP_HOSTNAME
            port = 80
        else:
            hostname = "localhost"
            port = 8000
        Site.objects.create(
            hostname=hostname,
            port=port,
            root_page=home_page,
            site_name="Foundation Home Page",
            is_default_site=True,
        )

    return home_page
