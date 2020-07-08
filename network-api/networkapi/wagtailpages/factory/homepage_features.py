from factory import SubFactory
from factory.django import DjangoModelFactory

from networkapi.wagtailpages.models import (
    HomepageFeaturedHighlights,
    HomepageFeaturedBlogs,
    BlogPage
)
from networkapi.utility.faker.helpers import (
    reseed,
    get_homepage
)
from .blog import BlogPageFactory
from networkapi.highlights.factory import HighlightFactory
from .homepage import WagtailHomepageFactory


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
    print('Generating Homepage Blogs and Highlights')

    home_page = get_homepage()

    reseed(seed)

    NUM_BLOGS = 4
    NUM_HIGHLIGHTS = 5

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

    home_page.save()
