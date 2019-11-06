from random import randint, random, choice
from datetime import date, timezone
from django.conf import settings
from django.core.management import call_command

from factory import (
    DjangoModelFactory,
    Faker,
    post_generation,
    LazyAttribute,
    LazyFunction,
)

from networkapi.utility.faker import ImageProvider, generate_fake_data
from networkapi.utility.faker.helpers import reseed
from networkapi.buyersguide.models import (
    Product,
    BuyersGuideProductCategory,
    RangeVote,
    BooleanVote
)

Faker.add_provider(ImageProvider)


def get_extended_yes_no_value():
    options = ['Yes', 'No', 'NA', 'U']
    return choice(options)


class ProductFactory(DjangoModelFactory):

    class Meta:
        model = Product
        exclude = (
            'product_words'
        )

    product_words = Faker('words', nb=2)

    draft = Faker('boolean')
    adult_content = Faker('boolean')
    review_date = Faker('date_time_between_dates',
                        datetime_start=date(year=2018, month=11, day=1), datetime_end=None, tzinfo=timezone.utc)
    name = LazyAttribute(lambda o: ' '.join(o.product_words))

    @post_generation
    def product_category(self, create, extracted, **kwargs):
        """
        After model generation, Relate this product to one or more product categories.
        Do this in a way that will assign some products 2 or more categories.
        """
        ceiling = 1.0
        while True:
            odds = random()
            if odds < ceiling:
                category = choice(BuyersGuideProductCategory.objects.all())
                self.product_category.add(category)
                ceiling = ceiling / 5
            else:
                return

    blurb = Faker('sentence')

    camera_app = LazyFunction(get_extended_yes_no_value)
    camera_device = LazyFunction(get_extended_yes_no_value)
    microphone_app = LazyFunction(get_extended_yes_no_value)
    microphone_device = LazyFunction(get_extended_yes_no_value)
    location_app = LazyFunction(get_extended_yes_no_value)
    location_device = LazyFunction(get_extended_yes_no_value)

    company = Faker('company')
    delete_data = Faker('boolean')
    email = Faker('email')
    live_chat = Faker('url')
    manage_vulnerabilities = LazyFunction(get_extended_yes_no_value)
    meets_minimum_security_standards = Faker('boolean')
    parental_controls = LazyFunction(get_extended_yes_no_value)
    phone_number = Faker('phone_number')
    price = LazyAttribute(lambda _: randint(49, 1500))
    privacy_policy_reading_level = LazyAttribute(lambda _: str(randint(7, 15)))
    privacy_policy_reading_level_url = Faker('url')
    security_updates = LazyFunction(get_extended_yes_no_value)
    share_data = Faker('boolean')
    strong_password = LazyFunction(get_extended_yes_no_value)
    url = Faker('url')
    uses_encryption = LazyFunction(get_extended_yes_no_value)
    worst_case = Faker('sentence')

    @post_generation
    def set_image(self, create, extracted, **kwargs):
        if settings.USE_CLOUDINARY:
            self.cloudinary_image = Faker('product_image').generate({})
        else:
            self.image.name = Faker('product_image').generate({})


def generate(seed):
    reseed(seed)

    print('Generating fixed Buyer\'s Guide Product for visual regression testing')
    ProductFactory.create(
        adult_content=False,
        blurb='Visual Regression Testing',
        camera_app='Yes',
        camera_device='No',
        collects_biometrics='Yes',
        collects_biometrics_helptext='biometrics help text',
        company='Percy',
        delete_data=True,
        draft=False,
        email='vrt@example.com',
        live_chat='https://example.com/chat',
        location_app='U',
        location_device='NA',
        manage_vulnerabilities='Yes',
        meets_minimum_security_standards=True,
        microphone_app='Yes',
        microphone_device='No',
        name='percy cypress',
        parental_controls='NA',
        phone_number='1-555-555-5555',
        price=350,
        privacy_policy_reading_level_url='https://vrt.example.com/pprl',
        privacy_policy_reading_level='7',
        product_words=['Percy', 'Cypress'],
        security_updates='No',
        share_data=False,
        strong_password='No',
        url='https://vrt.example.com',
        uses_encryption='Yes',
        worst_case='Duplicate work that burns through screenshots',
    )

    reseed(seed)

    print('Generating Buyer\'s Guide Products')
    generate_fake_data(ProductFactory, 70)

    reseed(seed)

    print('Generating Randomised Buyer\'s Guide Products Votes')
    for p in Product.objects.all():
        for _ in range(1, 15):
            value = randint(1, 100)
            RangeVote.objects.create(
                product=p,
                attribute='creepiness',
                value=value
            )

            value = (random() < 0.5)
            BooleanVote.objects.create(
                product=p,
                attribute='confidence',
                value=value
            )

    reseed(seed)

    print('Aggregating Buyer\'s Guide Product votes')
    call_command('aggregate_product_votes')
