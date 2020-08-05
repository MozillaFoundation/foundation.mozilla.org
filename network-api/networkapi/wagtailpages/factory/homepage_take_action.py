from factory import Faker
from wagtail_factories import ImageFactory
from wagtail.images.models import Image
from wagtail.core.models import Page

from networkapi.wagtailpages.pagemodels.base import HomepageTakeActionCards
from networkapi.utility.faker.helpers import reseed, get_homepage


def generate(seed):
    print('Generating Homepage Take Actions')

    home_page = get_homepage()

    reseed(seed)

    for i in range(4):
        take_action_orderable = HomepageTakeActionCards.objects.create(
            page=home_page,
            image=Image.objects.order_by("?").first(),
            text=Faker('text', max_nb_chars=255).generate(),
            internal_link=Page.objects.order_by("?").first(),
        )
        home_page.take_action_cards.add(take_action_orderable)

    home_page.save()
