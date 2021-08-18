from factory import Faker
from factory.django import DjangoModelFactory

from networkapi.wagtailpages.models import ContentAuthor
from networkapi.utility.faker import generate_fake_data
from networkapi.utility.faker.helpers import reseed

NUM_CONTENT_AUTHORS = 10


class ContentAuthorFactory(DjangoModelFactory):

    class Meta:
        model = ContentAuthor

    name = Faker('name')


def generate(seed):
    reseed(seed)

    print('Generating Content Authors')
    generate_fake_data(ContentAuthorFactory, NUM_CONTENT_AUTHORS)
