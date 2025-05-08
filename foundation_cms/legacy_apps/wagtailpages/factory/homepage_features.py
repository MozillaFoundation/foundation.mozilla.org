from random import choice

from foundation_cms.legacy_apps.utility.faker.helpers import get_homepage, reseed
from foundation_cms.legacy_apps.wagtailpages.models import (
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
    HomepageFocusAreas.objects.create(page=home_page, area=FocusArea.objects.get(name="Rally Citizens"))

    HomepageFocusAreas.objects.create(page=home_page, area=FocusArea.objects.get(name="Connect Leaders"))

    HomepageFocusAreas.objects.create(page=home_page, area=FocusArea.objects.get(name="Shape the Agenda"))

    NUM_IDEAS_POSTS = 3

    all_blogs = list(BlogPage.objects.all())

    home_page.ideas_posts = [
        HomepageIdeasPosts.objects.create(page=home_page, blog=choice(all_blogs)) for i in range(NUM_IDEAS_POSTS)
    ]

    home_page.save()
