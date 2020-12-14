from random import randint, random, choice, randrange, shuffle
from datetime import date, timezone, timedelta
from django.conf import settings
# from django.core.management import call_command

from factory import (
    DjangoModelFactory,
    Faker,
    post_generation,
    LazyAttribute,
    LazyFunction,
)

from wagtail_factories import PageFactory

from networkapi.wagtailpages.pagemodels.base import Homepage
from networkapi.wagtailpages.pagemodels.products import (
    BuyersGuidePage,
    GeneralProductPage,
    ProductPage,
    ProductPageVotes,
    ProductPagePrivacyPolicyLink,
    RelatedProducts,
    SoftwareProductPage,
)
from networkapi.utility.faker import (
    ImageProvider,
    # generate_fake_data
)
from networkapi.utility.faker.helpers import reseed
from networkapi.buyersguide.models import (
    # Product,
    Update,
    ProductPrivacyPolicyLink,
    GeneralProduct,
    SoftwareProduct,
    BuyersGuideProductCategory,
    # RangeVote,
    # BooleanVote,
)

Faker.add_provider(ImageProvider)


def get_random_option(options=[]):
    return choice(options)


def get_extended_yes_no_value():
    return get_random_option(['Yes', 'No', 'NA', 'U'])


def get_lowest_content_category():
    return sorted(
        [
            (cat.published_product_count, cat)
            for cat in BuyersGuideProductCategory.objects.all()
        ],
        key=lambda t: t[0]
    )[0][1]


class ProductPrivacyPolicyLinkFactory(DjangoModelFactory):
    class Meta:
        model = ProductPrivacyPolicyLink

    label = Faker('sentence')
    url = Faker('url')


class ProductUpdateFactory(DjangoModelFactory):
    class Meta:
        model = Update

    source = Faker('url')
    title = Faker('sentence')
    author = Faker('sentence')
    featured = Faker('boolean')
    snippet = Faker('sentence')


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = GeneralProduct
        exclude = (
            'product_words'
        )

    product_words = Faker('words', nb=2)

    draft = Faker('boolean')
    privacy_ding = Faker('boolean')
    adult_content = Faker('boolean')
    uses_wifi = Faker('boolean')
    uses_bluetooth = Faker('boolean')
    review_date = Faker('date_time_between_dates',
                        datetime_start=date(year=2020, month=11, day=1), datetime_end=None, tzinfo=timezone.utc)
    name = LazyAttribute(lambda o: ' '.join(o.product_words))
    company = Faker('company')

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
                category = get_lowest_content_category()
                self.product_category.add(category)
                ceiling = ceiling / 5
            else:
                return

    blurb = Faker('sentence')
    url = Faker('url')
    price = LazyAttribute(lambda _: randint(49, 1500))

    @post_generation
    def set_image(self, create, extracted, **kwargs):
        if settings.USE_CLOUDINARY:
            self.cloudinary_image = Faker('product_image').generate({})
        else:
            self.image.name = Faker('product_image').generate({})

    worst_case = Faker('sentence')

    signup_requires_email = LazyFunction(get_extended_yes_no_value)
    signup_requires_phone = LazyFunction(get_extended_yes_no_value)
    signup_requires_third_party_account = LazyFunction(get_extended_yes_no_value)
    signup_requirement_explanation = Faker('sentence')

    how_does_it_use_data_collected = Faker('sentence')
    data_collection_policy_is_bad = Faker('boolean')
    user_friendly_privacy_policy = LazyFunction(get_extended_yes_no_value)

    meets_minimum_security_standards = Faker('boolean')
    show_ding_for_minimum_security_standards = Faker('boolean')
    uses_encryption = LazyFunction(get_extended_yes_no_value)
    uses_encryption_helptext = Faker('sentence')
    security_updates = LazyFunction(get_extended_yes_no_value)
    security_updates_helptext = Faker('sentence')
    strong_password = LazyFunction(get_extended_yes_no_value)
    strong_password_helptext = Faker('sentence')
    manage_vulnerabilities = LazyFunction(get_extended_yes_no_value)
    manage_vulnerabilities_helptext = Faker('sentence')
    privacy_policy = LazyFunction(get_extended_yes_no_value)
    privacy_policy_helptext = Faker('sentence')

    @post_generation
    def set_privacy_policy_link(self, create, extracted, **kwargs):
        ProductPrivacyPolicyLinkFactory.create(product=self)

    phone_number = Faker('phone_number')
    live_chat = Faker('url')
    email = Faker('email')

    if random() > 0.5:
        twitter = '@TwitterHandle',

    # updates...


class GeneralProductFactory(ProductFactory):
    class Meta:
        model = GeneralProduct

    camera_app = LazyFunction(get_extended_yes_no_value)
    camera_device = LazyFunction(get_extended_yes_no_value)
    microphone_app = LazyFunction(get_extended_yes_no_value)
    microphone_device = LazyFunction(get_extended_yes_no_value)
    location_app = LazyFunction(get_extended_yes_no_value)
    location_device = LazyFunction(get_extended_yes_no_value)

    personal_data_collected = Faker('sentence')
    biometric_data_collected = Faker('sentence')
    social_data_collected = Faker('sentence')

    how_can_you_control_your_data = Faker('sentence')
    data_control_policy_is_bad = Faker('boolean')

    company_track_record = LazyFunction(lambda: get_random_option([
        'Great',
        'Average',
        'Needs Improvement',
        'Bad',
    ]))
    track_record_is_bad = Faker('boolean')
    track_record_details = Faker('sentence')

    offline_capable = LazyFunction(get_extended_yes_no_value)
    offline_use_description = Faker('sentence')

    @post_generation
    def set_privacy_policy_link(self, create, extracted, **kwargs):
        ProductPrivacyPolicyLinkFactory.create(product=self)

    uses_ai = LazyFunction(get_extended_yes_no_value)
    ai_uses_personal_data = LazyFunction(get_extended_yes_no_value)
    ai_is_transparent = LazyFunction(get_extended_yes_no_value)
    ai_helptext = Faker('sentence')


class SoftwareProductFactory(ProductFactory):
    class Meta:
        model = SoftwareProduct

    handles_recordings_how = Faker('sentence')
    recording_alert = LazyFunction(get_extended_yes_no_value)
    recording_alert_helptext = Faker('sentence')
    medical_privacy_compliant = Faker('boolean')
    medical_privacy_compliant_helptext = Faker('sentence')
    host_controls = Faker('sentence')
    easy_to_learn_and_use = Faker('boolean')
    easy_to_learn_and_use_helptext = Faker('sentence')


class BuyersGuidePageFactory(PageFactory):

    class Meta:
        model = BuyersGuidePage


class ProductPageVotesFactory(DjangoModelFactory):

    class Meta:
        model = ProductPageVotes

    vote_bins = LazyFunction(lambda: ','.join([str(randint(1, 50)) for x in range(0, 5)]))


class ProductPageFactory(PageFactory):

    class Meta:
        model = ProductPage

    title = Faker('sentence')

    privacy_ding = Faker('boolean')
    adult_content = Faker('boolean')
    uses_wifi = Faker('boolean')
    uses_bluetooth = Faker('boolean')
    company = Faker('company')
    blurb = Faker('sentence')
    product_url = Faker('url')
    price = LazyAttribute(lambda _: randint(49, 1500))
    worst_case = Faker('sentence')

    first_published_at = Faker('past_datetime', start_date='-2d', tzinfo=timezone.utc)
    last_published_at = Faker('past_datetime', start_date='-1d', tzinfo=timezone.utc)

    # TODO: add image binding

    @post_generation
    def set_random_review_date(self, create, extracted, **kwargs):
        start_date = date(2020, 10, 1)
        end_date = date(2021, 1, 30)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = randrange(days_between_dates)
        self.review_date = start_date + timedelta(days=random_number_of_days)

    @post_generation
    def set_random_creepiness(self, create, extracted, **kwargs):
        self.get_or_create_votes()
        single_vote = [0, 0, 0, 0, 1]
        shuffle(single_vote)
        self.votes.set_votes(single_vote)
        self.creepiness_value = randint(0, 100)


class GeneralProductPageFactory(ProductPageFactory):

    class Meta:
        model = GeneralProductPage

    camera_app = LazyFunction(get_extended_yes_no_value)
    camera_device = LazyFunction(get_extended_yes_no_value)
    microphone_app = LazyFunction(get_extended_yes_no_value)
    microphone_device = LazyFunction(get_extended_yes_no_value)
    location_app = LazyFunction(get_extended_yes_no_value)
    location_device = LazyFunction(get_extended_yes_no_value)
    personal_data_collected = Faker('sentence')
    biometric_data_collected = Faker('sentence')
    social_data_collected = Faker('sentence')
    how_can_you_control_your_data = Faker('sentence')
    data_control_policy_is_bad = Faker('boolean')
    company_track_record = get_random_option(['Great', 'Average', 'Needs Improvement', 'Bad'])
    track_record_is_bad = Faker('boolean')
    track_record_details = Faker('sentence')
    offline_capable = LazyFunction(get_extended_yes_no_value)
    offline_use_description = Faker('sentence')
    uses_ai = LazyFunction(get_extended_yes_no_value)
    ai_uses_personal_data = LazyFunction(get_extended_yes_no_value)
    ai_is_transparent = LazyFunction(get_extended_yes_no_value)
    ai_helptext = Faker('sentence')
    email = Faker('email')
    live_chat = Faker('url')
    phone_number = Faker('phone_number')
    twitter = '@TwitterHandle'


class SoftwareProductPageFactory(ProductPageFactory):

    class Meta:
        model = SoftwareProductPage

    price = 0

    handles_recordings_how = Faker('sentence')
    recording_alert = LazyFunction(get_extended_yes_no_value)
    recording_alert_helptext = Faker('sentence')
    medical_privacy_compliant = Faker('boolean')
    medical_privacy_compliant_helptext = Faker('sentence')
    host_controls = Faker('sentence')
    easy_to_learn_and_use = Faker('boolean')
    easy_to_learn_and_use_helptext = Faker('sentence')
    handles_recordings_how = Faker('sentence')
    recording_alert = LazyFunction(get_extended_yes_no_value)
    recording_alert_helptext = Faker('sentence')
    medical_privacy_compliant = Faker('boolean')
    medical_privacy_compliant_helptext = Faker('sentence')
    host_controls = Faker('sentence')
    easy_to_learn_and_use = Faker('boolean')
    easy_to_learn_and_use_helptext = Faker('sentence')


class ProductPagePrivacyPolicyLinkFactory(DjangoModelFactory):

    class Meta:
        model = ProductPagePrivacyPolicyLink

    label = Faker('sentence')
    url = Faker('url')


def generate(seed):
    reseed(seed)

    print('Generating PNI Homepage')
    pni_homepage = BuyersGuidePageFactory.create(
        parent=Homepage.objects.first(),
        title='* Privacy not included',
        slug='privacynotincluded',
    )

    print('Generating 100 ProductPages')
    for i in range(50):
        # Create 50 GeneralProductPages with Privacy Link Orderables
        general_page = GeneralProductPageFactory.create(
            parent=pni_homepage,
        )
        fake_privacy_policy = ProductPagePrivacyPolicyLinkFactory(
            page=general_page
        )
        general_page.privacy_policy_links.add(fake_privacy_policy)
        general_page.save_revision().publish()
        # Create 50 SoftwareProductPages with Privacy Link Orderables
        software_page = SoftwareProductPageFactory.create(
            parent=pni_homepage,
        )
        software_page.save_revision().publish()
        fake_privacy_policy = ProductPagePrivacyPolicyLinkFactory(
            page=software_page
        )
        software_page.privacy_policy_links.add(fake_privacy_policy)
        software_page.save_revision().publish()

    print('Adding related products to ProductPages')
    product_pages = ProductPage.objects.all()
    total_product_pages = product_pages.count()
    for product_page in product_pages:
        # Create a new orderable 3 times.
        # Each page will be randomly selected from an existing factory page.
        for i in range(3):
            random_number = randint(1, total_product_pages) - 1
            random_page = product_pages[random_number]
            related_product = RelatedProducts(
                page=product_page,
                related_product=random_page,
            )
            related_product.save()
            product_page.related_product_pages.add(related_product)

    """
    The following code is no longer necessary, as we will not need to test against the old
    PNI anymore. However, the percy data will have to be reinstated in immediate follow-up.

    print('Generating fixed Buyer\'s Guide GeneralProduct for visual regression testing')
    GeneralProductFactory.create(
        blurb='Visual Regression Testing',
        company='Percy',
        draft=False,
        email='percy@example.com',
        live_chat='https://example.com/percy/chat',
        name='percy cypress',
        phone_number='1-555-555-5555',
        price=350,
        product_words=['Percy', 'Cypress'],
        url='https://example.com/percy',
        twitter='@TwitterHandle',
        worst_case='Duplicate work that burns through screenshots'
    )

    print('Generating fixed Buyer\'s Guide SoftwareProduct for visual regression testing')
    SoftwareProductFactory.create(
        blurb='Visual Regression Testing',
        company='Percy',
        draft=False,
        email='percy@example.com',
        live_chat='https://example.com/percy/chat',
        name='percy cypress app',
        phone_number='1-555-555-5555',
        price='| Free',
        product_words=['Percy', 'Cypress'],
        url='https://example.com/percy',
        twitter='@TwitterHandle',
        worst_case='Duplicate work that burns through screenshots'
    )

    reseed(seed)

    print('Generating Buyer\'s Guide product updates')
    generate_fake_data(ProductUpdateFactory, 15)

    reseed(seed)

    print('Generating Buyer\'s Guide Products')
    generate_fake_data(GeneralProductFactory, 70)

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
    """
