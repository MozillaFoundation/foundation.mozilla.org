from factory import (
    Faker
)
from networkapi.utility.faker.helpers import reseed, get_homepage


def generate(seed):
    print('Generating Homepage Cause Statement Link')

    home_page = get_homepage()

    reseed(seed)

    home_page.cause_statement_link_text = Faker('text', max_nb_chars=80)
    home_page.cause_statement_link_page = home_page.get_descendants().order_by("?").first()
    home_page.save()
