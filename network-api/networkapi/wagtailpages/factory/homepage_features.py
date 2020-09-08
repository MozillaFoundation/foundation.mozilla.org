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

    HomepageFocusAreas.objects.create(
        page=home_page,
        area=empower_action
    )

    HomepageFocusAreas.objects.create(
        page=home_page,
        area=connect_leaders
    )

    HomepageFocusAreas.objects.create(
        page=home_page,
        area=investigate_and_research
    )

    NUM_SPOTLIGHT_POSTS = 3

    home_page.spotlight_posts = [
        HomepageSpotlightPosts.objects.create(
            page=home_page,
            blog=BlogPage.objects.order_by("?").first()
        )
        for i in range(NUM_SPOTLIGHT_POSTS)
    ]

    home_page.save()
