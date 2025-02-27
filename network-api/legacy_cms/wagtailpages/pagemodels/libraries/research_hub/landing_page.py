from functools import cached_property

from wagtail.admin import panels
from wagtail_localize import fields as localize_fields

from legacy_cms.wagtailpages.pagemodels.libraries import (
    landing_page as base_landing_page,
)
from legacy_cms.wagtailpages.pagemodels.libraries.research_hub import authors_index
from legacy_cms.wagtailpages.pagemodels.libraries.research_hub import (
    detail_page as rcc_detail_page,
)
from legacy_cms.wagtailpages.pagemodels.libraries.research_hub import (
    library_page as rcc_library_page,
)


class ResearchLandingPage(base_landing_page.BaseLandingPage):
    subpage_types = [
        "ResearchLibraryPage",
        "ResearchAuthorsIndexPage",
    ]

    template = "pages/libraries/research_hub/landing_page.html"

    content_panels = base_landing_page.BaseLandingPage.content_panels + [
        panels.InlinePanel("featured_topics", heading="Featured topics"),
        panels.InlinePanel("featured_authors", heading="Featured authors", max_num=4),
    ]

    translatable_fields = base_landing_page.BaseLandingPage.translatable_fields + [
        localize_fields.TranslatableField("featured_topics"),
        localize_fields.TranslatableField("featured_authors"),
    ]

    @cached_property
    def library_page(self):
        """Return the library page that this landing page is for."""
        return rcc_library_page.ResearchLibraryPage.objects.filter(locale=self.locale).first()

    @cached_property
    def detail_pages(self):
        """Return the detail pages that are children of this page."""
        return rcc_detail_page.ResearchDetailPage.objects.filter(locale=self.locale).live().public()

    @cached_property
    def authors_detail_url_name(self):
        return "research-author-detail"

    @cached_property
    def authors_index_page(self):
        return authors_index.ResearchAuthorsIndexPage.objects.first()
