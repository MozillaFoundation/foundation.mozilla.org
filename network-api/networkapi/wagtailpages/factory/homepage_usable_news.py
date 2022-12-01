from factory import SubFactory
from factory.django import DjangoModelFactory

from networkapi.utility.faker.helpers import get_homepage, reseed
from networkapi.wagtailpages.models import BlogPage, HomepageNewsYouCanUse

from .blog import BlogPageFactory
from .homepage import WagtailHomepageFactory


class NewsYouCanUseFactory(DjangoModelFactory):
    class Meta:
        abstract = True

    page = SubFactory(WagtailHomepageFactory)


class HomepageNewsYouCanUseFactory(NewsYouCanUseFactory):
    class Meta:
        model = HomepageNewsYouCanUse

    blog = SubFactory(BlogPageFactory)


def generate(seed):
    print("Generating Homepage Blogs and Highlights")

    home_page = get_homepage()

    reseed(seed)

    home_page.news_you_can_use = [HomepageNewsYouCanUseFactory.build(blog=BlogPage.objects.all()[i]) for i in range(4)]

    home_page.save()
