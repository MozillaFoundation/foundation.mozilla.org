from django.conf import settings
from wagtail.core.models import (
    Page as WagtailPage,
    Site as WagtailSite
)
from wagtail_factories import (
    PageFactory,
    ImageFactory
)
from factory import (
    Faker,
    SubFactory,
    LazyAttribute
)
from .models import (
    MozfestHomepage,
    MozfestPrimaryPage
)
from networkapi.utility.faker import StreamfieldProvider
from networkapi.utility.faker.helpers import reseed

streamfield_fields = ['paragraph', 'image', 'spacer', 'quote']
Faker.add_provider(StreamfieldProvider)


class MozfestPrimaryPageFactory(PageFactory):
    class Meta:
        model = MozfestPrimaryPage
        exclude = ('header_text')

    header = LazyAttribute(lambda o: o.header_text.rstrip('.'))
    banner = SubFactory(ImageFactory)
    intro = Faker('paragraph', nb_sentences=3, variable_nb_sentences=False)
    body = Faker('streamfield', fields=streamfield_fields)
    header_text = Faker('sentence', nb_words=6, variable_nb_words=True)


class MozfestHomepageFactory(MozfestPrimaryPageFactory):
    class Meta:
        model = MozfestHomepage
        exclude = (
            'header_text',
            'banner_heading_text'
        )

    banner_heading = 'Come with an idea, leave with a community.'
    # LazyAttribute(lambda o: o.banner_heading_text.rstrip('.'))
    banner_guide_text = ('Now in its 10th year, the Mozilla Festival is a seven-day '
                         'gathering of educators, activists, technologists, artists, and '
                         'young people dedicated to creating a better, healthier open internet.')
    # Faker('paragraph', nb_sentences=10, variable_nb_sentences=True)
    banner_video_url = Faker('url')
    prefooter_text = Faker('paragraph', nb_sentences=5, variable_nb_sentences=True)
    banner_heading_text = Faker('sentence', nb_words=6, variable_nb_words=True)


def generate(seed):
    reseed(seed)

    print('Generating Mozfest Homepage')
    try:
        home_page = MozfestHomepage.objects.get(title='Mozilla Festival')
        print('Homepage already exists')
    except MozfestHomepage.DoesNotExist:
        print('Generating a Homepage')
        site_root = WagtailPage.objects.get(title='Root')
        home_page = MozfestHomepageFactory.create(
            parent=site_root,
            title='Mozilla Festival',
            slug=None
        )

    reseed(seed)

    print('Creating MozFest Site record in Wagtail')
    tds = settings.TARGET_DOMAINS
    if tds and len(tds) > 1:
        # Assume that tds[0] is the main mofo domain, and tds[1] is the Mozfest domain
        hostname = tds[1]
        port = 80
    else:
        # use a localhost domain (must be set in /etc/hosts)
        hostname = 'mozfest.localhost'
        port = 8000

    WagtailSite.objects.create(
        hostname=hostname,
        port=port,
        root_page=home_page,
        site_name='Mozilla Festival',
        is_default_site=False
    )

    print('Generating Mozfest sub-pages')
    [MozfestPrimaryPageFactory.create(
        parent=home_page,
        title=title
    ) for title in ['About', 'Spaces', 'Tickets', 'Team', 'Sponsors']]
