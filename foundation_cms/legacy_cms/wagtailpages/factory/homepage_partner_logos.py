from random import choice

from faker import Faker  # note: NOT from factory, but from faker. Different Faker!
from wagtail.images.models import Image

from foundation_cms.legacy_cms.utility.faker.helpers import get_homepage, reseed
from foundation_cms.legacy_cms.wagtailpages.models import PartnerLogos

faker = Faker()


def generate(seed):
    print("Generating Partner Logos")

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
