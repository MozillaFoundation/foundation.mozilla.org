import random

from factory import (
    DjangoModelFactory,
    Faker,
    post_generation,
    LazyAttribute,
)

from networkapi.utility.faker_providers import ImageProvider
from networkapi.buyersguide.models import Product

Faker.add_provider(ImageProvider)


class ProductFactory(DjangoModelFactory):

    class Meta:
        model = Product
        exclude = (
            'product_words'
        )

    product_words = Faker('words', nb=2)

    name = LazyAttribute(lambda o: ' '.join(o.product_words))
    company = Faker('company')
    blurb = Faker('sentence')
    url = Faker('url')
    price = random.randint(49, 1500)
    camera = Faker('boolean')
    microphone = Faker('boolean')
    location = Faker('boolean')
    need_account = Faker('boolean')
    privacy_controls = Faker('boolean')
    delete_data = Faker('boolean')
    share_data = Faker('boolean')
    child_rules = Faker('boolean')
    privacy_policy = Faker('url')
    worst_case = Faker('sentence')

    @post_generation
    def set_image(self, create, extracted, **kwargs):
        self.image.name = Faker('generic_image').generate({})
