import random
from django.conf import settings

from factory import (
    DjangoModelFactory,
    Faker,
    post_generation,
    LazyAttribute,
)

from networkapi.utility.faker_providers import ImageProvider
from networkapi.buyersguide.models import (
    Product,
    BuyersGuideProductCategory
)

Faker.add_provider(ImageProvider)


def get_random_category():
    all = BuyersGuideProductCategory.objects.all()
    total = all.count()
    index = random.randint(0, total-1)
    return all[index]


class ProductFactory(DjangoModelFactory):

    class Meta:
        model = Product
        exclude = (
            'product_words'
        )

    product_words = Faker('words', nb=2)

    name = LazyAttribute(lambda o: ' '.join(o.product_words))

    @post_generation
    def product_category(self, create, extracted, **kwargs):
        """
        After model generation, Relate this product to one or more product categories.
        Do this in a way that will assign some products 2 or more categories.
        """
        ceiling = 1.0
        while True:
            odds = random.random()
            if odds < ceiling:
                category = get_random_category()
                self.product_category.add(category)
                ceiling = ceiling / 5
            else:
                return

    company = Faker('company')
    blurb = Faker('sentence')
    url = Faker('url')
    price = random.randint(49, 1500)
    camera_app = Faker('boolean')
    meets_minimum_security_standards = Faker('boolean')
    camera_device = Faker('boolean')
    microphone_app = Faker('boolean')
    microphone_device = Faker('boolean')
    location_app = Faker('boolean')
    location_device = Faker('boolean')
    uses_encryption = Faker('boolean')
    privacy_policy_reading_level_url = Faker('url')
    privacy_policy_reading_level = str(random.randint(7, 19))
    share_data = Faker('boolean')
    must_change_default_password = Faker('boolean')
    security_updates = Faker('boolean')
    delete_data = Faker('boolean')
    child_rules = Faker('boolean')
    manage_security = Faker('boolean')
    phone_number = Faker('phone_number')
    live_chat = Faker('url')
    email = Faker('email')
    worst_case = Faker('sentence')

    @post_generation
    def set_image(self, create, extracted, **kwargs):
        if settings.USE_CLOUDINARY:
            self.cloudinary_image = Faker('generic_image').generate({})
        else:
            self.image.name = Faker('generic_image').generate({})
