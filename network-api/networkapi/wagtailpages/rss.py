from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.text import Truncator

from .models import BlogIndexPage


class RSSFeed(Feed):
    """
    Blog page RSS feed, using the content:encoded serializer above
    """

    title = 'Mozilla Foundation Blog'
    link = 'https://foundation.mozilla.org/blog/'
    feed_url = 'https://foundation.mozilla.org/blog/rss/'
    description = 'The Mozilla Foundation Blog'

    def items(self):
        # Pull this object specifically using the English page title
        blog_index = BlogIndexPage.objects.get(title_en__iexact='Blog')

        # If that doesn't yield the blog page, pull using the universal title
        if blog_index is None:
            blog_index = BlogIndexPage.objects.get(title__iexact='Blog')

        blog_pages = blog_index.get_all_entries()
        return blog_pages[:settings.FEED_LIMIT]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.full_url

    def item_description(self, item):
        page = item.specific
        html = str(page.body)
        text = Truncator(html).chars(1000, html=True)
        return text

    def item_pubdate(self, item):
        return item.first_published_at


class AtomFeed(RSSFeed):
    feed_type = Atom1Feed
    link = RSSFeed.link
    feed_url = 'https://foundation.mozilla.org/blog/atom/'
    subtitle = RSSFeed.description
