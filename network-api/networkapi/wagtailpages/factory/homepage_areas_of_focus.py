from networkapi.wagtailpages.models import FocusArea, AreaOfFocus
from networkapi.utility.faker.helpers import reseed, get_homepage


def generate(seed):
    print('Generating Homepage Areas of Focus')

    home_page = get_homepage()

    reseed(seed)

    for i in range(3):
        focus_area = FocusArea.objects.order_by("?").first()
        focus_area_orderable = AreaOfFocus.objects.create(
            page=home_page,
            area=focus_area,
        )
        home_page.areas_of_focus.add(focus_area_orderable)
    home_page.save()
