from random import choice
from factory import Faker
from networkapi.utility.faker.helpers import reseed, get_homepage


def generate(seed):
    print('Generating Homepage Cause Statement Link')

    home_page = get_homepage()

    reseed(seed)

    home_page.cause_statement_link_text = Faker('text', max_nb_chars=80)

    all_children = list(home_page.get_descendants())

    home_page.cause_statement_link_page = choice(all_children)
    home_page.save()
