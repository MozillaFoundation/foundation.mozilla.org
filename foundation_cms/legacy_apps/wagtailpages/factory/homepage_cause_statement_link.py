from random import choice

from faker import Faker  # note: NOT from factory, but from faker. Different Faker!

from foundation_cms.legacy_apps.utility.faker.helpers import get_homepage, reseed

faker = Faker()


def generate(seed):
    print("Generating Homepage Cause Statement Link")

    home_page = get_homepage()

    reseed(seed)

    home_page.cause_statement_link_text = faker.text(max_nb_chars=80)

    all_children = list(home_page.get_descendants())

    home_page.cause_statement_link_page = choice(all_children)
    home_page.save()
