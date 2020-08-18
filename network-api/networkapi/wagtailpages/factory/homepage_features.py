from factory import SubFactory
from factory.django import DjangoModelFactory

from networkapi.wagtailpages.models import (
    FocusArea,
    HomepageFocusAreas,
    HomepageFeaturedHighlights,
    HomepageFeaturedBlogs,
    HomepageSpotlightPosts,
    BlogPage,
)
from networkapi.utility.faker.helpers import (
    reseed,
    get_homepage
)
from .blog import BlogPageFactory
from networkapi.highlights.factory import HighlightFactory
from .homepage import (
    WagtailHomepageFactory
)


class FeaturedFactory(DjangoModelFactory):
    class Meta:
        abstract = True

    page = SubFactory(WagtailHomepageFactory)


class HomepageFeaturedBlogsFactory(FeaturedFactory):
    class Meta:
        model = HomepageFeaturedBlogs

    blog = SubFactory(BlogPageFactory)


class HomepageFeaturedHighlightsFactory(FeaturedFactory):
    class Meta:
        model = HomepageFeaturedHighlights

    highlight = SubFactory(HighlightFactory)


def generate(seed):
    print('Generating Homepage Blogs, Highlights and Spotlights')

    home_page = get_homepage()

    reseed(seed)

    # These are "guaranteed" to exist as they are created as
    # part of the wagtailpages migrations:
    HomepageFocusAreas.objects.create(
        page=home_page,
        area=FocusArea.objects.get(name='Empower Action')
    )

    HomepageFocusAreas.objects.create(
        page=home_page,
        area=FocusArea.objects.get(name='Connect Leaders')
    )

    HomepageFocusAreas.objects.create(
        page=home_page,
        area=FocusArea.objects.get(name='Investigate & Research')
    )

    NUM_BLOGS = 4
    NUM_HIGHLIGHTS = 5
    NUM_SPOTLIGHT_POSTS = 3

    home_page.featured_blogs = [
        HomepageFeaturedBlogsFactory.build(
            blog=BlogPage.objects.all()[i]
        )
        for i in range(NUM_BLOGS)
    ]

    home_page.featured_highlights = [
        HomepageFeaturedHighlightsFactory.build(
            highlight=HighlightFactory.create()
        )
        for i in range(NUM_HIGHLIGHTS)
    ]

    home_page.spotlight_posts = [
        HomepageSpotlightPosts.objects.create(
            page=home_page,
            blog=BlogPage.objects.order_by("?").first()
        )
        for i in range(NUM_SPOTLIGHT_POSTS)
    ]

    home_page.save()
