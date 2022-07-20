from datetime import timezone
from random import choice

from django.conf import settings
from wagtail.core.models import Page as WagtailPage
from wagtail_factories import PageFactory
from factory import (
    Faker,
    LazyAttribute,
)
from factory.django import DjangoModelFactory

from networkapi.wagtailpages.models import (
    BlogAuthors,
    BlogPage,
    BlogPageTopic,
    BlogIndexPage,
    Profile,
)
from networkapi.wagtailpages.pagemodels.blog import blog_index
from networkapi.utility.faker.helpers import (
    get_homepage,
    get_random_objects,
    reseed
)
from .index_page import IndexPageFactory
from .tagging import add_tags


RANDOM_SEED = settings.RANDOM_SEED
TESTING = settings.TESTING
blog_body_streamfield_fields = [
    'paragraph',
    'image',
    'image_text',
    'image_text_mini',
    'video',
    'linkbutton',
    'spacer',
    'quote',
]


def add_topic(post):
    topic_choices = BlogPageTopic.objects.all()
    post.topics.add(choice(topic_choices))
    post.save()


def add_related_topics(blog_index):
    topics_to_add = BlogPageTopic.objects.all()[:5]
    for topic in topics_to_add:
        blog_index.related_topics.add(topic)
    blog_index.save()


def add_authors(post):
    for profile in get_random_objects(model=Profile, max_count=5):
        author_orderable = BlogAuthors.objects.create(page=post, author=profile)
        post.authors.add(author_orderable)

    post.save()


def add_featured_posts(blog_index_page):
    for page in BlogPage.objects.all()[:5]:
        featured_page_orderable = blog_index.FeaturedBlogPages.objects.create(page=blog_index_page, blog=page)
        blog_index_page.featured_pages.add(featured_page_orderable)

    blog_index_page.save()


class BlogIndexPageFactory(IndexPageFactory):
    class Meta:
        model = BlogIndexPage

    callout_box = Faker('streamfield', fields=['callout_box'])


class BlogPageFactory(PageFactory):

    class Meta:
        model = BlogPage
        exclude = (
            'title_text',
        )

    title = LazyAttribute(lambda o: o.title_text.rstrip('.'))
    body = Faker('streamfield', fields=blog_body_streamfield_fields)
    first_published_at = (Faker('date_time', tzinfo=timezone.utc) if RANDOM_SEED and not TESTING
                          else Faker('past_datetime', start_date='-30d', tzinfo=timezone.utc))
    search_description = (Faker('paragraph', nb_sentences=5, variable_nb_sentences=True))
    live = True

    # Lazy Values
    title_text = Faker('sentence', nb_words=3, variable_nb_words=False)


class FeaturedBlogPagesFactory(DjangoModelFactory):
    class Meta:
        model = blog_index.FeaturedBlogPages


class FeaturedVideoPostFactory(DjangoModelFactory):
    class Meta:
        model = blog_index.FeaturedVideoPost


class BlogPageTopicFactory(DjangoModelFactory):
    class Meta:
        model = BlogPageTopic


def generate(seed):
    reseed(seed)
    home_page = get_homepage()

    try:
        blog_namespace = WagtailPage.objects.get(title='Blog')
        print('blog namespace exists')
    except WagtailPage.DoesNotExist:
        print('Generating a blog namespace')
        blog_namespace = BlogIndexPageFactory.create(
            parent=home_page,
            title='Blog',
            header='Blog',
            show_in_menus=True,
            live=True
        )

    add_related_topics(blog_namespace)

    print('Generating blog posts under namespace')
    title = 'Initial test blog post with fixed title'
    post = None

    try:
        post = BlogPage.objects.get(title=title)
    except BlogPage.DoesNotExist:
        post = BlogPageFactory.create(parent=blog_namespace, title=title)

    add_tags(post)
    add_topic(post)
    add_authors(post)

    for i in range(6):
        title = Faker('sentence', nb_words=6, variable_nb_words=False)
        post = None

        try:
            post = BlogPage.objects.get(title=title)
        except BlogPage.DoesNotExist:
            post = BlogPageFactory.create(parent=blog_namespace, title=title)

        add_tags(post)
        add_topic(post)
        add_authors(post)

    for post in BlogPage.objects.all():
        post.ensure_related_posts()
        post.save()

    add_featured_posts(blog_namespace)
