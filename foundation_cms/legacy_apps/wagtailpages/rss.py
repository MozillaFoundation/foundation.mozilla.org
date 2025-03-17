from django.conf import settings
from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.utils.feedgenerator import Atom1Feed
from wagtail.models import Locale

from foundation_cms.legacy_apps.wagtailpages.utils import get_locale_from_request

from .models import BlogIndexPage, IndexPage


class RSSFeed(Feed):
    """
    Blog page RSS feed, using the content:encoded serializer above
    """

    title = "Mozilla Foundation Blog"
    description = "The Mozilla Foundation Blog"

    def __call__(self, request, *args, **kwargs):
        # get locale from request header, or fall back to the default EN locale.
        request_locale = get_locale_from_request(request)
        setattr(self, "request_locale", request_locale)
        return super().__call__(request, *args, **kwargs)

    @property
    def link(self):
        blog_index_page = self.get_blog_index_page()
        return blog_index_page.url

    @property
    def feed_url(self):
        return f"{self.link}/rss/"

    def get_blog_index_page(self):
        blog_index = BlogIndexPage.objects.get(locale=Locale.get_default())
        return blog_index

    def items(self):
        # Get locale from request in __call__ above, defaults to EN.
        request_locale = getattr(self, "request_locale")

        # Try to get the RSS items from cache first
        feed_set = cache.get("rss_feed_set")

        if feed_set is None:
            # If we don't have an active cache, we build one: First, retrieve the BlogIndexPage.
            try:
                blog_index = self.get_blog_index_page()

            except BlogIndexPage.DoesNotExist:
                # If that doesn't yield the blog index page, there's not much we can do other than to pretend
                # there are no posts to serialize to RSS/Atom format.
                return []

            # Because BlogIndexPage overrides the get_all_entries method to exclude "featured" posts
            # for its "Featured Posts" section, we directly use IndexPage's get_all_entries method.
            # This ensures that all posts, including those categorized as "featured", are included.
            blog_pages = IndexPage.get_all_entries(blog_index, request_locale).order_by("-first_published_at")

            # Then sort the collection and only yield the top FEED_LIMIT posts
            feed_set = blog_pages[: settings.FEED_LIMIT]

            cache.set("rss_feed_set", feed_set, settings.FEED_CACHE_TIMEOUT)

        return feed_set

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
    feed_url = f"{link}/atom/"
    subtitle = RSSFeed.description
