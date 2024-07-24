from functools import cached_property

from wagtail.admin import panels
from wagtail_localize import fields as localize_fields

from networkapi.wagtailpages.pagemodels.libraries import (
    landing_page as base_landing_page,
)
from networkapi.wagtailpages.pagemodels.libraries.rcc import authors_index
from networkapi.wagtailpages.pagemodels.libraries.rcc import (
    detail_page as rcc_detail_page,
)
from networkapi.wagtailpages.pagemodels.libraries.rcc import (
    library_page as rcc_library_page,
)


class RCCLandingPage(base_landing_page.BaseLandingPage):
    subpage_types = [
        "RCCLibraryPage",
        "RCCAuthorsIndexPage",
    ]

    template = "pages/libraries/rcc/landing_page.html"

    content_panels = base_landing_page.BaseLandingPage.content_panels + [
        panels.MultipleChooserPanel(
            "featured_content_types", heading="Featured content types", chooser_field_name="content_type"
        ),
        panels.MultipleChooserPanel(
            "featured_authors", heading="Featured authors", chooser_field_name="author", max_num=4
        ),
    ]

    translatable_fields = base_landing_page.BaseLandingPage.translatable_fields + [
        localize_fields.TranslatableField("featured_content_types"),
        localize_fields.TranslatableField("featured_authors"),
    ]

    class Meta(base_landing_page.BaseLandingPage.Meta):
        verbose_name = "RCC landing page"
        verbose_name_plural = "RCC landing pages"

    @cached_property
    def library_page(self):
        """Return the library page that this landing page is for."""
        return rcc_library_page.RCCLibraryPage.objects.filter(locale=self.locale).first()

    @cached_property
    def detail_pages(self):
        """Return the detail pages that are children of this page."""
        return rcc_detail_page.RCCDetailPage.objects.filter(locale=self.locale).live().public()

    @cached_property
    def authors_detail_url_name(self):
        return "rcc-author-detail"

    @cached_property
    def authors_index_page(self):
        return authors_index.RCCAuthorsIndexPage.objects.first()
