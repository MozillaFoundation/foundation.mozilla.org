import wagtail_factories
import factory
from wagtail.models import Page
from .models import BlogIndexPage, BlogPage
from foundation_cms.profiles.factories import ProfileFactory


class BlogIndexPageFactory(wagtail_factories.PageFactory):
    """
    Factory for BlogIndexPage
    """
    class Meta:
        model = BlogIndexPage

    title = factory.Faker("sentence", nb_words=3)
    slug = factory.Faker("slug")
    body = factory.Faker("paragraph")


class BlogPageFactory(wagtail_factories.PageFactory):
    """
    Factory for BlogPage
    """
    class Meta:
        model = BlogPage

    title = factory.Faker("sentence", nb_words=4)
    slug = factory.Faker("slug")
    body = factory.Faker("paragraph")
    author = factory.SubFactory(ProfileFactory)


def create_blog_with_posts(blog_page_count=5):
    """
    Create a BlogIndexPage under the default HomePage and generate BlogPages.
    Manually included and called in the clean_install.sh script
    @TODO establish more robust factory workflow
    """
    # Fetch the default Wagtail home page
    home_page = Page.objects.get(depth=2)

    # Create a BlogIndexPage
    blog_index = BlogIndexPageFactory(parent=home_page)

    # Create the blog pages
    BlogPageFactory.create_batch(blog_page_count, parent=blog_index)