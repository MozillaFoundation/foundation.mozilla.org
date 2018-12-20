import random
from django.conf import settings
from django.core.management import call_command

from factory import (
    DjangoModelFactory,
    Faker,
    post_generation,
    LazyAttribute,
)

from networkapi.utility.faker import ImageProvider, generate_fake_data
from networkapi.buyersguide.models import (
    Product,
    BuyersGuideProductCategory,
    RangeVote,
    BooleanVote
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
            self.cloudinary_image = Faker('product_image').generate({})
        else:
            self.image.name = Faker('product_image').generate({})


def generate():
    print('Generating Buyer\'s Guide Products')
    generate_fake_data(ProductFactory, 70)

    print('Generating Randomised Buyer\'s Guide Products Votes')
    for p in Product.objects.all():
        for _ in range(1, 15):
            value = random.randint(1, 100)
            RangeVote.objects.create(
                product=p,
                attribute='creepiness',
                value=value
            )

            value = (random.random() < 0.5)
            BooleanVote.objects.create(
                product=p,
                attribute='confidence',
                value=value
            )

    print('Aggregating Buyer\'s Guide Product votes')
    call_command('aggregate_product_votes')
