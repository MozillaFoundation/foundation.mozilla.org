from wagtail.core.models import Page
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from networkapi.wagtailpages.utils import get_locale_from_request, get_default_locale
from .blog import BlogPage


class MockSearchBlogIndex(RoutablePageMixin, Page):

    template = 'wagtailpages/mock_search_blog_index.html'

    def search_pages(self, locale, search_query):
        return BlogPage.objects.live().public().filter(locale=locale).search(search_query)

    @route(r"^search/$")
    def blog_page_search(self, request, *args, **kwargs):
        search_query = request.GET.get("q", None)

        if search_query:
            self.search_term = search_query
            self.search_type = 'search'

            (DEFAULT_LOCALE, _) = get_default_locale()
            current_locale = get_locale_from_request(request)
            self.results = self.search_pages(current_locale, search_query)

            if current_locale != DEFAULT_LOCALE:
                self.default_results = self.search_pages(DEFAULT_LOCALE, search_query)

        return self.render(request)
