from networkapi.wagtailpages.models import InitiativesPage
from wagtail_factories import PageFactory, ImageFactory
from wagtail.core.models import Page as WagtailPage
from factory import (
    Faker,
    SubFactory
)
from networkapi.utility.faker.helpers import (
    reseed,
    get_homepage
)


class InitiativesPageFactory(PageFactory):
    class Meta:
        model = InitiativesPage

    title = 'initiatives'

    sectionImage = SubFactory(ImageFactory)
    sectionHeader = Faker('text', max_nb_chars=20)
    sectionCopy = Faker('text', max_nb_chars=300)
    sectionButtonTitle = Faker('text', max_nb_chars=8)
    sectionButtonURL = Faker('url')
    sectionButtonTitle2 = Faker('text', max_nb_chars=10)
    sectionButtonURL2 = Faker('url')


def generate(seed):
    home_page = get_homepage()
    reseed(seed)

    try:
        WagtailPage.objects.get(title='initiatives')
        print('initiatives page exists')
    except WagtailPage.DoesNotExist:
        print('Generating an empty Initiatives Page')
        InitiativesPageFactory.create(parent=home_page)
