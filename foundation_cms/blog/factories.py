import factory
import wagtail_factories
from wagtail.models import Locale

from foundation_cms.base.models import HomePage
from foundation_cms.profiles.factories import ProfileFactory

from .models import BlogIndexPage, BlogPage


class BlogIndexPageFactory(wagtail_factories.PageFactory):
    """
    Factory for BlogIndexPage
    """

    class Meta:
        model = BlogIndexPage

    title = factory.Faker("sentence", nb_words=3)
    slug = "blog"
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

    # Retrieve the default locale
    default_locale = Locale.get_default()

    # Get the homepage for the default locale
    home_page = HomePage.objects.filter(locale=default_locale).first()

    if home_page:
        # Create a BlogIndexPage for the default locale's homepage
        blog_index = BlogIndexPageFactory(parent=home_page, title=f"Blog Index for {default_locale.language_code}")

        # Create the blog pages and attach them to the blog index page
        BlogPageFactory.create_batch(blog_page_count, parent=blog_index)
    else:
        print(f"No homepage found for default locale {default_locale.language_code}")
