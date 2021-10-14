from random import choice

from networkapi.wagtailpages.models import (
    FocusArea,
    HomepageFocusAreas,
    HomepageSpotlightPosts,
    BlogPage,
)

from networkapi.utility.faker.helpers import (
    reseed,
    get_homepage
)


def generate(seed):
    print('Generating Homepage Focus Areas and Spotlights')

    home_page = get_homepage()

    reseed(seed)

    # These are "guaranteed" to exist as they are created as
    # part of the wagtailpages migrations:
    HomepageFocusAreas.objects.create(
        page=home_page,
        area=FocusArea.objects.get(name='Rally Citizens')
    )

    HomepageFocusAreas.objects.create(
        page=home_page,
        area=FocusArea.objects.get(name='Connect Leaders')
    )

    HomepageFocusAreas.objects.create(
        page=home_page,
        area=FocusArea.objects.get(name='Shape the Agenda')
    )

    NUM_SPOTLIGHT_POSTS = 3

    all_blogs = list(BlogPage.objects.all())

    home_page.spotlight_posts = [
        HomepageSpotlightPosts.objects.create(
            page=home_page,
            blog=choice(all_blogs)
        )
        for i in range(NUM_SPOTLIGHT_POSTS)
    ]

    home_page.save()
