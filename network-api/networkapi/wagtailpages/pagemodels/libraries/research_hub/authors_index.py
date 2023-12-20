import typing
from functools import cached_property

from wagtail.contrib.routable_page import models as routable_models

from networkapi.wagtailpages import utils
from networkapi.wagtailpages.pagemodels.libraries import (
    authors_index as base_authors_index_page,
)
from networkapi.wagtailpages.pagemodels.libraries.research_hub import library_page
from networkapi.wagtailpages.pagemodels.libraries.research_hub import (
    utils as research_utils,
)

if typing.TYPE_CHECKING:
    from django import http


class ResearchAuthorsIndexPage(base_authors_index_page.BaseAuthorsIndexPage):
    parent_page_types = ["ResearchLandingPage"]

    template = "pages/libraries/research_hub/authors_index_page.html"

    @cached_property
    def author_profiles(self):
        """Return the author profiles associated with this library.

        Author profiles should be localised via the `utils.localize_queryset` method.
        When the index is displayed in a non-default locale, then want to show
        the profile associated with that locale. But, profiles do not necessarily
        exist in all locales. We prefer showing the profile for the locale, but fall
        back to the profile on the default locale.
        """
        return utils.localize_queryset(research_utils.get_research_authors()).order_by("name")

    @cached_property
    def library_page(self):
        """Return the library page that this index page is for."""
        return library_page.ResearchLibraryPage.objects.child_of(self.get_parent()).live().public().first()

    @routable_models.route(r"^(?P<profile_slug>[-a-z0-9]+)/$", name="research-author-detail")
    def author_detail(self, request: "http.HttpRequest", profile_slug: str) -> "http.HttpResponse":
        context_overrides = self.get_author_detail_context(profile_slug=profile_slug)

        return self.render(
            request=request,
            template="pages/libraries/research_hub/author_detail_page.html",
            context_overrides=context_overrides,
        )
