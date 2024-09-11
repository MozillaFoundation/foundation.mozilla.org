from random import choice

from networkapi.utility.faker.helpers import get_homepage, reseed
from networkapi.wagtailpages.models import (
    BlogPage,
    FocusArea,
    HomepageFocusAreas,
    HomepageIdeasPosts,
)


def generate(seed):
    print("Generating Homepage Focus Areas and Spotlights")

    home_page = get_homepage()

    reseed(seed)

    # These are "guaranteed" to exist as they are created as
    # part of the wagtailpages migrations:
    HomepageFocusAreas.objects.create(page=home_page, area=FocusArea.objects.get(name="$25.2 million"))

    HomepageFocusAreas.objects.create(page=home_page, area=FocusArea.objects.get(name="150 fellows"))

    HomepageFocusAreas.objects.create(page=home_page, area=FocusArea.objects.get(name="100,000+ signatures"))

    NUM_IDEAS_POSTS = 3

    all_blogs = list(BlogPage.objects.all())

    home_page.ideas_posts = [
        HomepageIdeasPosts.objects.create(page=home_page, blog=choice(all_blogs)) for i in range(NUM_IDEAS_POSTS)
    ]

    home_page.save()
