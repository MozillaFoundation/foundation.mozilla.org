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
    empower_action, created = FocusArea.objects.get_or_create(
        name='Empower Action',
        defaults={
            'name': 'Empower Action #2',
            'description': 'Lorem',
            'page': home_page,
        }
    )
    connect_leaders, created = FocusArea.objects.get_or_create(
        name='Connect Leaders',
        defaults={
            'name': 'Connect Leaders #2',
            'description': 'Lorem',
            'page': home_page,
        }
    )
    investigate_and_research, created = FocusArea.objects.get_or_create(
        name='Investigate & Research',
        defaults={
            'name': 'Investigate & Research #2',
            'description': 'Lorem',
            'page': home_page,
        }
    )

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
