from random import choice

from wagtail.images.models import Image

from networkapi.wagtailpages.models import (
    PartnerLogos,
)

from networkapi.utility.faker.helpers import (
    reseed,
    get_homepage
)

from faker import Faker  # note: NOT from factory, but from faker. Different Faker!
faker = Faker()


def generate(seed):
    print('Generating Partner Logos')

    home_page = get_homepage()

    reseed(seed)

    all_images = list(Image.objects.all())

    for i in range(3):
        partner_logo_orderable = PartnerLogos.objects.create(
            page=home_page,
            logo=choice(all_images),
            link=faker.url(),
            name=faker.text(max_nb_chars=30),
        )
        home_page.partner_logos.add(partner_logo_orderable)

    home_page.save()
