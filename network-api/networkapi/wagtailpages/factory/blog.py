from datetime import timezone
from random import shuffle, choice
from django.conf import settings
from wagtail_factories import PageFactory
from factory import (
    Faker,
    LazyAttribute
)
from wagtail.core.models import Page as WagtailPage

from networkapi.wagtailpages.models import BlogPage, BlogPageCategory
from networkapi.utility.faker.helpers import (
    get_homepage,
    reseed
)
from .index_page import IndexPageFactory

RANDOM_SEED = settings.RANDOM_SEED
TESTING = settings.TESTING

blog_body_streamfield_fields = ['paragraph', 'image', 'image_text', 'image_text_mini',
                                'video', 'linkbutton', 'spacer', 'quote']

tags = [
    'mozilla', 'iot', 'privacy', 'security', 'internet health',
    'digital inclusion', 'advocacy', 'policy']


def add_tags(post):
    shuffle(tags)

    for tag in tags[0:3]:
        post.tags.add(tag)

    post.save()


def add_category(post):
    categories = BlogPageCategory.objects.all()
    post.category.add(choice(categories))
    post.save()


class BlogPageFactory(PageFactory):

    class Meta:
        model = BlogPage
        exclude = (
            'title_text',
        )

    title = LazyAttribute(lambda o: o.title_text.rstrip('.'))
    author = Faker('name')
    body = Faker('streamfield', fields=blog_body_streamfield_fields)
    first_published_at = (Faker('date_time', tzinfo=timezone.utc) if RANDOM_SEED and not TESTING
                          else Faker('past_datetime', start_date='-30d', tzinfo=timezone.utc))
    live = True

    # Lazy Values
    title_text = Faker('sentence', nb_words=3, variable_nb_words=False)


def generate(seed):
    reseed(seed)
    home_page = get_homepage()

    try:
        blog_namespace = WagtailPage.objects.get(title='blog')
        print('blog namespace exists')
    except WagtailPage.DoesNotExist:
        print('Generating a blog namespace')
        blog_namespace = IndexPageFactory.create(
            parent=home_page,
            title='Blog',
            header='Blog',
            live=True
        )

    print('Generating blog posts under namespace')
    title = 'Initial test blog post with fixed title'

    post = None

    try:
        post = BlogPage.objects.get(title=title)
        print('test blog post page exists')
    except BlogPage.DoesNotExist:
        print('test blog post page does not exist')
        post = BlogPageFactory.create(parent=blog_namespace, title=title)
        print('test blog post page created')

    # add_tags(post)
    # add_category(post)
