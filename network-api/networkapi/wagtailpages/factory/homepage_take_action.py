from random import choice
from wagtail.images.models import Image
from wagtail.core.models import Page

from networkapi.wagtailpages.pagemodels.base import HomepageTakeActionCards
from networkapi.utility.faker.helpers import reseed, get_homepage

from faker import Faker  # note: NOT from factory, but from faker. Different Faker!

faker = Faker()


def generate(seed):
    print('Generating Homepage Take Actions')

    home_page = get_homepage()

    reseed(seed)

    all_images = list(Image.objects.all())
    all_pages = list(Page.objects.all())

    for i in range(4):
        take_action_orderable = HomepageTakeActionCards.objects.create(
            page=home_page,
            image=choice(all_images),
            text=faker.text(max_nb_chars=255),
            internal_link=choice(all_pages),
        )
        home_page.take_action_cards.add(take_action_orderable)

    home_page.save()
