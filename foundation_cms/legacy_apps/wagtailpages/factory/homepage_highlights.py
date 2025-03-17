from factory import SubFactory
from factory.django import DjangoModelFactory

from foundation_cms.legacy_apps.utility.faker.helpers import get_homepage, reseed
from foundation_cms.legacy_apps.wagtailpages.models import BlogPage, HomepageHighlights

from .blog import BlogPageFactory
from .homepage import WagtailHomepageFactory


class HightlightsFactory(DjangoModelFactory):
    class Meta:
        abstract = True

    page = SubFactory(WagtailHomepageFactory)


class HomepageHightlightsFactory(HightlightsFactory):
    class Meta:
        model = HomepageHighlights

    blog = SubFactory(BlogPageFactory)


def generate(seed):
    print("Generating Homepage Blogs and Highlights")

    home_page = get_homepage()

    reseed(seed)

    home_page.highlights = [HomepageHightlightsFactory.build(blog=BlogPage.objects.all()[i]) for i in range(4)]

    home_page.save()
