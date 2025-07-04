from datetime import timedelta
from random import randint, random, shuffle

from django.conf import settings
from factory import Faker, SubFactory, post_generation
from wagtail_factories import PageFactory

from foundation_cms.legacy_apps.utility.faker.helpers import (
    get_homepage,
    get_random_date,
    reseed,
)
from foundation_cms.legacy_apps.wagtailpages.factory.documents import DocumentFactory
from foundation_cms.legacy_apps.wagtailpages.factory.image_factory import ImageFactory
from foundation_cms.legacy_apps.wagtailpages.models import (
    ArticlePage,
    Profile,
    PublicationPage,
)
from foundation_cms.legacy_apps.wagtailpages.pagemodels.publications.article import (
    ArticleAuthors,
)

RANDOM_SEED = settings.RANDOM_SEED
TESTING = settings.TESTING
article_body_streamfield_fields = [
    "content",
    "double_image",
    "callout",
    "content",
    "full_width_image",
    "image_grid",
    "image_text",
]


class PublicationPageFactory(PageFactory):
    title = Faker("text", max_nb_chars=120)
    subtitle = Faker("text", max_nb_chars=250)
    secondary_subtitle = Faker("text", max_nb_chars=250)
    publication_date = get_random_date()
    hero_image = SubFactory(ImageFactory)
    publication_file = SubFactory(DocumentFactory)
    intro_notes = Faker("sentence")
    notes = Faker("sentence")

    @post_generation
    def toc_thumbnail_image(self, create, extracted, **kwargs):
        if random() < 0.5:
            self.toc_thumbnail_image = ImageFactory()

    class Meta:
        model = PublicationPage


class ArticlePageFactory(PageFactory):
    class Meta:
        model = ArticlePage

    title = Faker("text", max_nb_chars=60)
    hero_image = SubFactory(ImageFactory)
    subtitle = Faker("text", max_nb_chars=250)
    secondary_subtitle = Faker("text", max_nb_chars=250)
    publication_date = get_random_date()
    article_file = SubFactory(DocumentFactory)
    body = Faker("streamfield", fields=article_body_streamfield_fields)
    first_published_at = publication_date - timedelta(days=10)
    search_description = Faker("paragraph", nb_sentences=5, variable_nb_sentences=True)
    live = True

    @post_generation
    def toc_thumbnail_image(self, create, extracted, **kwargs):
        if random() < 0.5:
            self.toc_thumbnail_image = ImageFactory()


def add_authors(post):
    authors = list(Profile.objects.all())
    count = len(authors)

    shuffle(authors)

    for i in range(0, randint(1, min(count, 5))):
        author_orderable = ArticleAuthors.objects.create(page=post, author=authors[i])
        post.authors.add(author_orderable)

    post.save()


def generate(seed):
    """
    Makes a batch of publication pages and article pages.
    """

    reseed(seed)
    home_page = get_homepage()

    """
    Create a couple scenarios that will be best for testing:
    * A PublicationPage with several child ArticlePages
    * A PublicationPage with child PublicationPages, each of which has their own ArticlePages
        * future: perhaps nested at random levels of depth?
    """

    reseed(seed)

    fixed_title_article_page = "Fixed title article page"
    fixed_title_chapter_page = "Fixed title chapter page"

    pub_page_with_child_articles = PublicationPageFactory.create(
        parent=home_page, title="Publication Page with child Article Pages"
    )

    pub_page_with_chapters = PublicationPageFactory.create(
        parent=home_page, title="Publication Page with chapter pages"
    )
    PublicationPageFactory.create(parent=pub_page_with_chapters, title=fixed_title_chapter_page)
    PublicationPageFactory.create_batch(parent=pub_page_with_chapters, size=3)

    reseed(seed)

    ArticlePageFactory.create(parent=pub_page_with_child_articles, title=fixed_title_article_page)
    ArticlePageFactory.create_batch(parent=pub_page_with_child_articles, size=8)

    for chapter in pub_page_with_chapters.get_children():
        ArticlePageFactory.create(parent=chapter, title=fixed_title_article_page)
        ArticlePageFactory.create_batch(parent=chapter, size=8)

    article_pages = ArticlePage.objects.all()
    for post in article_pages:
        add_authors(post)
