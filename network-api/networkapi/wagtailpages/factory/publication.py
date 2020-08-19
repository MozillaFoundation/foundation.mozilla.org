from networkapi.wagtailpages.pagemodels.publications.publication import PublicationPage
from wagtail_factories import PageFactory
from networkapi.utility.faker.helpers import (
    get_homepage,
    reseed
)
from factory import (
    Faker
)


class PublicationPageFactory(PageFactory):
    title = Faker('text', max_nb_chars=255)

    class Meta:
        model = PublicationPage


def generate(seed):
    reseed(seed)
    home_page = get_homepage()

    PublicationPageFactory.create_batch(parent=home_page, size=3)
