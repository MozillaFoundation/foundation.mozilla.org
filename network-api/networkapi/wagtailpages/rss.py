from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from .models import BlogPage


class RSSFeed(Feed):
    """
    Blog page RSS feed, using the content:encoded serializer above
    """

    title = 'Mozilla Foundation Blog'
    link = 'https://foundation.mozilla.org/blog/'
    feed_url = 'https://foundation.mozilla.org/blog/rss/'
    description = 'The Mozilla Foundation Blog'

    def items(self):
        return BlogPage.objects.live().public()[:settings.FEED_LIMIT]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.full_url

    def item_description(self, item):
        return item.get_meta_description()

    def item_pubdate(self, item):
        return item.first_published_at


class AtomFeed(RSSFeed):
    feed_type = Atom1Feed
    link = RSSFeed.link
    feed_url = 'https://foundation.mozilla.org/blog/atom/'
    subtitle = RSSFeed.description
