from datetime import timezone
from random import choice

from django.conf import settings

from wagtail.core.models import Page as WagtailPage

from wagtail_factories import PageFactory

from factory import (
    Faker,
    LazyAttribute
)

from networkapi.wagtailpages.models import (
    BlogAuthors,
    BlogPage,
    BlogPageCategory,
    BlogIndexPage,
    Profile,
)

from networkapi.utility.faker.helpers import (
    get_homepage,
    get_random_objects,
    reseed
)
from networkapi.wagtailpages.factory import profiles as profiles_factory

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


def add_category(post):
    categories = BlogPageCategory.objects.all()
    post.category.add(choice(categories))
    post.save()


def add_authors(post):
    for profile in get_random_objects(model=Profile, max_count=5):
        author_orderable = BlogAuthors.objects.create(page=post, author=profile)
        post.authors.add(author_orderable)

    post.save()


class BlogIndexPageFactory(IndexPageFactory):
    class Meta:
        model = BlogIndexPage


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

    print('Generating blog posts under namespace')
    title = 'Initial test blog post with fixed title'
    post = None

    try:
        post = BlogPage.objects.get(title=title)
    except BlogPage.DoesNotExist:
        post = BlogPageFactory.create(parent=blog_namespace, title=title)

    add_tags(post)
    add_category(post)
    add_authors(post)

    for i in range(6):
        title = Faker('sentence', nb_words=6, variable_nb_words=False)
        post = None

        try:
            post = BlogPage.objects.get(title=title)
        except BlogPage.DoesNotExist:
            post = BlogPageFactory.create(parent=blog_namespace, title=title)

        add_tags(post)
        add_category(post)
        add_authors(post)

    for post in BlogPage.objects.all():
        post.ensure_related_posts()
        post.save()
