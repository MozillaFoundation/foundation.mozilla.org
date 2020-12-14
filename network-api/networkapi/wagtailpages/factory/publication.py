from datetime import timezone
from random import randint, shuffle

from django.conf import settings

from wagtail.core.models import Collection
from wagtail_factories import PageFactory, ImageFactory
from networkapi.wagtailpages.models import ArticlePage, BlogAuthor, PublicationPage
from networkapi.utility.faker.helpers import get_homepage, reseed
from factory import (
    Faker,
    SubFactory,
    django,
    DjangoModelFactory,
)

from networkapi.wagtailpages.pagemodels.publications.article import ArticleAuthors

# UGLY COPYPASTE FROM latest
# https://github.com/mvantellingen/wagtail-factories/blob/master/src/wagtail_factories/factories.py

from wagtail_factories.factories import MP_NodeFactory

from wagtail.documents import get_document_model

RANDOM_SEED = settings.RANDOM_SEED
TESTING = settings.TESTING
article_body_streamfield_fields = [
    'content',
    'double_image',
    'callout',
    'content',
    'full_width_image',
]


class CollectionFactory(MP_NodeFactory):
    name = Faker('text', max_nb_chars=60)

    class Meta:
        model = Collection


class CollectionMemberFactory(DjangoModelFactory):
    collection = SubFactory(CollectionFactory, parent=None)


class DocumentFactory(CollectionMemberFactory):
    class Meta:
        model = get_document_model()

    title = Faker('text', max_nb_chars=250)
    file = django.FileField(
        filename=Faker('file_name', category='text'), file_extension="pdf"
    )


class PublicationPageFactory(PageFactory):
    title = Faker('text', max_nb_chars=120)
    subtitle = Faker('text', max_nb_chars=250)
    secondary_subtitle = Faker('text', max_nb_chars=250)
    publication_date = Faker('date_object')
    hero_image = SubFactory(ImageFactory)
    publication_file = DocumentFactory()

    class Meta:
        model = PublicationPage


class ArticlePageFactory(PageFactory):
    class Meta:
        model = ArticlePage

    title = Faker('text', max_nb_chars=60)
    body = Faker('streamfield', fields=article_body_streamfield_fields)
    first_published_at = (Faker('date_time', tzinfo=timezone.utc) if RANDOM_SEED and not TESTING
                          else Faker('past_datetime', start_date='-30d', tzinfo=timezone.utc))
    search_description = (Faker('paragraph', nb_sentences=5, variable_nb_sentences=True))
    live = True


def add_authors(post):
    authors = list(BlogAuthor.objects.all())
    count = len(authors)

    shuffle(authors)

    for i in range(0, randint(1, min(count, 5))):
        author_orderable = ArticleAuthors.objects.create(page=post, author=authors[i])
        post.authors.add(author_orderable)

    post.save()


def generate(seed):
    """
    Makes a batch of 3 publication pages.
    """

    reseed(seed)
    home_page = get_homepage()
    """
    Create a couple scenarios that will be best for testing:
    * A PublicationPage with several child ArticlePages
    * A PublicationPage with child PublicationPages, each of which has their own ArticlePages
        * future: perhaps nested at random levels of depth?
    """

    pub_page_with_child_articles = PublicationPageFactory.create(
        parent=home_page, title='Publication Page with child Article Pages'
    )
    pub_page_with_chapters = PublicationPageFactory.create(
        parent=home_page, title='Publication Page with chapter pages'
    )

    fixed_title_article_page = 'Fixed title article page'
    fixed_title_chapter_page = 'Fixed title chapter page'

    ArticlePageFactory.create(parent=pub_page_with_child_articles, title=fixed_title_article_page)
    ArticlePageFactory.create_batch(parent=pub_page_with_child_articles, size=8)

    PublicationPageFactory.create(parent=pub_page_with_chapters, title=fixed_title_chapter_page)
    PublicationPageFactory.create_batch(parent=pub_page_with_chapters, size=3)

    for chapter in pub_page_with_chapters.get_children():
        ArticlePageFactory.create(parent=chapter, title=fixed_title_article_page)
        ArticlePageFactory.create_batch(parent=chapter, size=8)

    article_pages = ArticlePage.objects.all()
    for post in article_pages:
        add_authors(post)
