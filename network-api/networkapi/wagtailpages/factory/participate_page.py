from wagtail_factories import PageFactory
from factory import (
    Faker,
    SubFactory
)
from wagtail.core.models import Page as WagtailPage

from networkapi.wagtailpages.factory.image_factory import ImageFactory
from networkapi.wagtailpages.models import ParticipatePage2
from networkapi.utility.faker.helpers import (
    reseed,
    get_homepage
)


class ParticipatePage2Factory(PageFactory):
    class Meta:
        model = ParticipatePage2

    title = 'participate'
    h2 = Faker('text', max_nb_chars=20)
    h2Subheader = Faker('text', max_nb_chars=250)

    # first block
    ctaHero = SubFactory(ImageFactory)
    ctaHeroHeader = Faker('text', max_nb_chars=50)
    ctaButtonTitle = Faker('text', max_nb_chars=50)
    ctaButtonURL = Faker('url')

    # second block
    ctaHero2 = SubFactory(ImageFactory)
    ctaHeroHeader2 = Faker('text', max_nb_chars=50)
    ctaButtonTitle2 = Faker('text', max_nb_chars=50)
    ctaButtonURL2 = Faker('url')

    # third block
    ctaHero3 = SubFactory(ImageFactory)
    ctaHeroHeader3 = Faker('text', max_nb_chars=50)
    ctaHeroSubhead3 = Faker('paragraph', nb_sentences=5, variable_nb_sentences=True)
    ctaFacebook3 = Faker('text', max_nb_chars=20)
    ctaTwitter3 = Faker('text', max_nb_chars=20)
    ctaEmailShareBody3 = Faker('text', max_nb_chars=20)
    ctaEmailShareSubject3 = Faker('text', max_nb_chars=50)

    # TODO: reduce all this duplication


def generate(seed):
    home_page = get_homepage()
    reseed(seed)

    try:
        WagtailPage.objects.get(title='participate')
        print('participate page exists')
    except WagtailPage.DoesNotExist:
        print('Generating an empty Participate Page')
        ParticipatePage2Factory.create(parent=home_page)
