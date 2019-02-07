from random import randint
from django.conf import settings

from factory import (
    DjangoModelFactory,
    Faker,
    post_generation,
    LazyAttribute,
)

from faker import Faker as ValueFaker

from networkapi.utility.faker import ImageProvider
from networkapi.buyersguide.models import (
    Product,
    BuyersGuideProductCategory
)

Faker.add_provider(ImageProvider)


seed = randint(0, 5000000)
if settings.RANDOM_SEED is not None:
    seed = settings.RANDOM_SEED

fake = ValueFaker()
fake.random.seed(seed)


def get_random_category():
    all = BuyersGuideProductCategory.objects.all()
    total = all.count()
    index = fake.unix_time() % total
    return all[index]


def get_random_float():
    window = 100000
    base = fake.unix_time() % (window + 1)
    return base / window


def get_random_int(s, e):
    return s + (fake.unix_time() % (e - s + 1))


class ProductFactory(DjangoModelFactory):

    class Meta:
        model = Product
        exclude = (
            'product_words'
        )

    product_words = Faker('words', nb=2)

    draft = Faker('boolean')
    adult_content = Faker('boolean')
    name = LazyAttribute(lambda o: ' '.join(o.product_words))

    @post_generation
    def product_category(self, create, extracted, **kwargs):
        """
        After model generation, Relate this product to one or more product categories.
        Do this in a way that will assign some products 2 or more categories.
        """
        ceiling = 1.0
        while True:
            odds = get_random_float()
            if odds < ceiling:
                category = get_random_category()
                self.product_category.add(category)
                ceiling = ceiling / 5
            else:
                return

    company = Faker('company')
    blurb = Faker('sentence')
    url = Faker('url')
    price = get_random_int(49, 1500)
    camera_app = Faker('boolean')
    meets_minimum_security_standards = Faker('boolean')
    camera_device = Faker('boolean')
    microphone_app = Faker('boolean')
    microphone_device = Faker('boolean')
    location_app = Faker('boolean')
    location_device = Faker('boolean')
    uses_encryption = Faker('boolean')
    privacy_policy_reading_level_url = Faker('url')
    privacy_policy_reading_level = str(get_random_int(7, 15))
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
            self.cloudinary_image = Faker('product_image').generate({})
        else:
            self.image.name = Faker('product_image').generate({})
