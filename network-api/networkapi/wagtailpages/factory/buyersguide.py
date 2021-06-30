# TODO: Move these factories to the wagtailpages app.
# To avoid too many code conflicts, this should happen after PR 6433 is merged
from random import randint, random, choice, randrange, shuffle
from datetime import date, datetime, timezone, timedelta

from factory import (
    DjangoModelFactory,
    Faker,
    post_generation,
    LazyAttribute,
    LazyFunction,
)

from wagtail.images.models import Image
from wagtail_factories import PageFactory

from networkapi.wagtailpages.factory.image_factory import ImageFactory
from networkapi.wagtailpages.pagemodels.base import Homepage
from networkapi.wagtailpages.pagemodels.products import (
    BuyersGuidePage,
    GeneralProductPage,
    BuyersGuideProductCategory,
    ProductPage,
    ProductPageVotes,
    ProductPagePrivacyPolicyLink,
    ProductUpdates,
    RelatedProducts,
    SoftwareProductPage,
)
from networkapi.utility.faker import ImageProvider, generate_fake_data
from networkapi.utility.faker.helpers import reseed

from networkapi.wagtailpages.pagemodels.products import Update
Faker.add_provider(ImageProvider)


def get_random_option(options=[]):
    return choice(options)


def get_extended_yes_no_value():
    return get_random_option(['Yes', 'No', 'NA', 'CD'])


def get_lowest_content_page_category():
    return sorted(
        [
            (cat.published_product_page_count, cat)
            for cat in BuyersGuideProductCategory.objects.all()
        ],
        key=lambda t: t[0]
    )[0][1]


class ProductUpdateFactory(DjangoModelFactory):
    class Meta:
        model = Update

    source = Faker('url')
    title = Faker('sentence')
    author = Faker('sentence')
    featured = Faker('boolean')
    snippet = Faker('sentence')


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

    @post_generation
    def assign_random_categories(self, create, extracted, **kwargs):
        # late import to prevent circular dependency
        from networkapi.wagtailpages.models import ProductPageCategory
        ceiling = 1.0
        while True:
            odds = random()
            if odds < ceiling:
                category = get_lowest_content_page_category()
                ProductPageCategory.objects.get_or_create(
                    product=self,
                    category=category
                )
                ceiling = ceiling / 5
            else:
                return

    @post_generation
    def set_random_review_date(self, create, extracted, **kwargs):
        if "Percy" not in self.title:
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


def create_general_product_visual_regression_product(seed, pni_homepage):
    # There are no random fields here: *everything* is prespecified
    GeneralProductPageFactory.create(
        # page fields
        title='General Percy Product',
        first_published_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
        last_published_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
        parent=pni_homepage,
        # product fields
        privacy_ding=True,
        adult_content=True,
        uses_wifi=True,
        uses_bluetooth=True,
        review_date=date(2025, 1, 1),
        company='Percy Corp',
        blurb='This is a general product specifically created for visual regression testing',
        product_url='http://example.com/general-percy',
        price=999,
        worst_case='Visual regression fails',
        # general product fields
        camera_app='Yes',
        camera_device='No',
        microphone_app='NA',
        microphone_device='CD',
        location_app='Yes',
        location_device='No',
        personal_data_collected='Is personal data getting collected?',
        biometric_data_collected='Is biometric data getting collected?',
        social_data_collected='Is social data getting collected?',
        how_can_you_control_your_data='So, how can you control your data?',
        data_control_policy_is_bad=True,
        company_track_record='Needs Improvement',
        track_record_is_bad=True,
        track_record_details='What kind of track record are we talking about?',
        offline_capable='Yes',
        offline_use_description='Although it is unclear how offline capabilities work',
        uses_ai='NA',
        ai_uses_personal_data='Yes',
        ai_is_transparent='No',
        ai_helptext='The AI is a black box and no one knows how it works',
        email='test@example.org',
        live_chat='http://example.org/chat',
        phone_number='1-555-555-5555',
        twitter='@TwitterHandle',
    )


def create_software_product_visual_regression_product(seed, pni_homepage):
    reseed(seed)
    SoftwareProductPageFactory.create(
        # page fields
        title='Software Percy Product',
        first_published_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
        last_published_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
        parent=pni_homepage,
        # product fields
        privacy_ding=True,
        adult_content=True,
        uses_wifi=True,
        uses_bluetooth=True,
        review_date=date(2025, 1, 1),
        company='Percy Corp',
        blurb='This is a general product specifically created for visual regression testing',
        product_url='http://example.com/general-percy',
        price=999,
        worst_case='Visual regression fails',
        # software product fields
    )


def generate(seed):
    reseed(seed)

    print('Generating PNI Homepage')
    pni_homepage = BuyersGuidePageFactory.create(
        parent=Homepage.objects.first(),
        title='* Privacy not included',
        slug='privacynotincluded',
        header='Be Smart. Shop Safe.',
        intro_text=(
            'How creepy is that smart speaker, that fitness tracker'
            ', those wireless headphones? We created this guide to help you shop for safe'
            ', secure connected products.'
        ),
    )

    print('Generating visual regression test products')
    create_general_product_visual_regression_product(seed, pni_homepage)
    create_software_product_visual_regression_product(seed, pni_homepage)

    print('Generating 52 ProductPages')
    for i in range(26):
        # General products
        general_page = GeneralProductPageFactory.create(parent=pni_homepage,)
        fake_privacy_policy = ProductPagePrivacyPolicyLinkFactory(page=general_page)
        general_page.privacy_policy_links.add(fake_privacy_policy)
        general_page.save_revision().publish()

        # Software products
        software_page = SoftwareProductPageFactory.create(parent=pni_homepage,)
        software_page.save_revision().publish()
        fake_privacy_policy = ProductPagePrivacyPolicyLinkFactory(page=software_page)
        software_page.privacy_policy_links.add(fake_privacy_policy)
        software_page.save_revision().publish()

    print('Crosslinking related products')
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

            # Create new ProductUpdates orderable for each PNI product
            product_update = ProductUpdates(
                page=product_page,
                update=ProductUpdateFactory()
            )
            product_update.save()
            product_page.updates.add(product_update)

            # Create three new privacy policy links for each PNI product
            privacy_orderable = ProductPagePrivacyPolicyLinkFactory(
                page=product_page,
            )
            privacy_orderable.save()
            product_page.privacy_policy_links.add(privacy_orderable)

    reseed(seed)

    print('Generating Buyer\'s Guide product updates')
    generate_fake_data(ProductUpdateFactory, 15)

    reseed(seed)

    print('Generating predictable PNI images')
    pni_images = Image.objects.filter(collection__name='pni products')
    for product_page in ProductPage.objects.all():
        if pni_images:
            product_page.image = choice(pni_images)
        else:
            product_page.image = ImageFactory()
        product_page.save()
    # TODO: link updates into products

    """
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
