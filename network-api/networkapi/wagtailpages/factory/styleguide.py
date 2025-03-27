import factory
from django.conf import settings
from wagtail.models import Page as WagtailPage
from wagtail_factories import PageFactory

from networkapi.utility.faker.helpers import get_homepage, reseed
from networkapi.wagtailpages.factory.image_factory import ImageFactory
from networkapi.wagtailpages.models import Styleguide

styleguide_streamfield_fields = [
    "paragraph",
    "image",
    "image_text",
    "image_text_mini",
    "image_grid",
    "video",
    "linkbutton",
    "spacer",
    "quote",
    "double_image",
    "text",
    "full_width_image",
    "card_grid",
    "pulse_listing",
    "profile_listing",
    "recent_blog_entries",
    "blog_set",
    "airtable",
    "typeform",
    "datawrapper",
]


class StyleguideFactory(PageFactory):
    class Meta:
        model = Styleguide

    title = "Style-guide"
    body = factory.Faker("streamfield", fields=styleguide_streamfield_fields)
    emoji_image = factory.SubFactory(
        ImageFactory,
        file=factory.django.ImageField(from_path=settings.BASE_DIR + "/../source/images/buyers-guide/heart-emoji.png"),
    )


def generate(seed):
    home_page = get_homepage()
    reseed(seed)

    try:
        WagtailPage.objects.get(title="Style-guide")
        print("styleguide page exists")
    except WagtailPage.DoesNotExist:
        print("Generating a Styleguide Page")
        StyleguideFactory.create(parent=home_page, show_in_menus=True)
