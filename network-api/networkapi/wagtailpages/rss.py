from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from .models import IndexPage


class RSSFeed(Feed):
    """
    Blog page RSS feed, using the content:encoded serializer above
    """

    title = 'Mozilla Foundation Blog'
    link = 'https://foundation.mozilla.org/blog/'
    feed_url = 'https://foundation.mozilla.org/blog/rss/'
    description = 'The Mozilla Foundation Blog'

    def items(self):
        # Pull this object specifically using the English page title, as an IndexPage
        # rather than a BlogIndexPage, to make sure we're not filtering out all the
        # "featured" posts (which we need to do for site content purposes))
        index = IndexPage.objects.get(title__iexact='Blog')

        # If that doesn't yield the blog page, pull using the universal title
        if index is None:
            index = IndexPage.objects.get(title__iexact='Blog')

        blog_pages = index.get_all_entries().order_by('-first_published_at')

        return blog_pages[:settings.FEED_LIMIT]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.full_url

    def item_description(self, item):
        page = item.specific
        html = str(page.body)
        return html

    def item_pubdate(self, item):
        return item.first_published_at


class AtomFeed(RSSFeed):
    feed_type = Atom1Feed
    link = RSSFeed.link
    feed_url = 'https://foundation.mozilla.org/blog/atom/'
    subtitle = RSSFeed.description
