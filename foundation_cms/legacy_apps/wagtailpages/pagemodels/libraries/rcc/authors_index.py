import typing
from functools import cached_property

from wagtail.contrib.routable_page import models as routable_models

from foundation_cms.legacy_apps.wagtailpages import utils
from foundation_cms.legacy_apps.wagtailpages.pagemodels.libraries import (
    authors_index as base_authors_index_page,
)
from foundation_cms.legacy_apps.wagtailpages.pagemodels.libraries.rcc import (
    library_page,
)
from foundation_cms.legacy_apps.wagtailpages.pagemodels.libraries.rcc import (
    utils as rcc_utils,
)

if typing.TYPE_CHECKING:
    from django import http


class RCCAuthorsIndexPage(base_authors_index_page.BaseAuthorsIndexPage):
    parent_page_types = ["RCCLandingPage"]

    template = "pages/libraries/rcc/authors_index_page.html"

    class Meta(base_authors_index_page.BaseAuthorsIndexPage.Meta):
        verbose_name = "RCC authors index page"
        verbose_name_plural = "RCC authors index pages"

    @cached_property
    def author_profiles(self):
        """Return the author profiles associated with this library.

        Author profiles should be localised via the `utils.localize_queryset` method.
        When the index is displayed in a non-default locale, then want to show
        the profile associated with that locale. But, profiles do not necessarily
        exist in all locales. We prefer showing the profile for the locale, but fall
        back to the profile on the default locale.
        """
        return utils.localize_queryset(rcc_utils.get_rcc_authors()).order_by("name")

    @cached_property
    def library_page(self):
        """Return the library page that this index page is for."""
        return library_page.RCCLibraryPage.objects.child_of(self.get_parent()).live().public().first()

    @routable_models.route(r"^(?P<profile_slug>[-a-z0-9]+)/$", name="rcc-author-detail")
    def author_detail(self, request: "http.HttpRequest", profile_slug: str) -> "http.HttpResponse":
        context_overrides = self.get_author_detail_context(profile_slug=profile_slug)

        return self.render(
            request=request,
            template="pages/libraries/rcc/author_detail_page.html",
            context_overrides=context_overrides,
        )
