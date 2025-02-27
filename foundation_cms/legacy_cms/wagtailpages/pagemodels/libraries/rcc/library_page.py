import typing
from functools import cached_property

from wagtail import models as wagtail_models

from legacy_cms.wagtailpages.pagemodels.libraries import (
    library_page as base_library_page,
)
from legacy_cms.wagtailpages.pagemodels.libraries.rcc import detail_page, taxonomies
from legacy_cms.wagtailpages.pagemodels.libraries.rcc import utils as rcc_utils
from legacy_cms.wagtailpages.pagemodels.libraries.rcc.forms import (
    RCCLibraryPageFilterForm,
)

if typing.TYPE_CHECKING:
    from django import forms
    from django.db.models.query import QuerySet


class RCCLibraryPage(base_library_page.BaseLibraryPage):
    parent_page_types = ["RCCLandingPage"]

    subpage_types = ["RCCDetailPage"]

    template = "pages/libraries/rcc/library_page.html"

    class Meta(base_library_page.BaseLibraryPage.Meta):
        verbose_name = "RCC library page"
        verbose_name_plural = "RCC library pages"

    @property
    def filter_form(self) -> "forms.Form":
        """Form class used to filter detail pages for this page."""
        return RCCLibraryPageFilterForm

    @cached_property
    def detail_pages(self) -> "QuerySet[detail_page.RCCDetailPage]":
        """Return the article detail pages that are children of this page."""
        return detail_page.RCCDetailPage.objects.live().public().filter(locale=wagtail_models.Locale.get_active())

    @staticmethod
    def filter_detail_pages(
        pages: "QuerySet[detail_page.RCCDetailPage]", filter_form: "forms.Form"
    ) -> "QuerySet[detail_page.RCCDetailPage]":
        """Return the article detail pages that match the given filters in the form."""
        if filter_form.is_valid():
            author_profile_ids: list[int] = filter_form.cleaned_data["authors"]
            content_type_ids: list[int] = filter_form.cleaned_data["content_types"]
            curricular_area_ids: list[int] = filter_form.cleaned_data["curricular_areas"]
            topic_ids: list[int] = filter_form.cleaned_data["topics"]
        else:
            # If the form is not valid, we will not filter by any of the values.
            # This will result in all articles being displayed.
            author_profile_ids = []
            content_type_ids = []
            curricular_area_ids = []
            topic_ids = []

        rcc_detail_pages = pages

        author_profiles = rcc_utils.get_rcc_authors()
        author_profiles = author_profiles.filter(id__in=author_profile_ids)
        for author_profile in author_profiles:
            # Synced but not translated pages are still associated with the default
            # locale's author profile. But, we want to show them when we are filtering
            # for the localized author profile. We use the fact that the localized and
            # default locale's author profile have the same `translation_key`.
            rcc_detail_pages = rcc_detail_pages.filter(
                authors__author_profile__translation_key=(author_profile.translation_key)
            )

        content_types = taxonomies.RCCContentType.objects.filter(id__in=content_type_ids)
        for content_type in content_types:
            rcc_detail_pages = rcc_detail_pages.filter(
                related_content_types__content_type__translation_key=content_type.translation_key
            )

        curricular_areas = taxonomies.RCCCurricularArea.objects.filter(id__in=curricular_area_ids)
        for curricular_area in curricular_areas:
            rcc_detail_pages = rcc_detail_pages.filter(
                related_curricular_areas__curricular_area__translation_key=curricular_area.translation_key
            )

        topics = taxonomies.RCCTopic.objects.filter(id__in=topic_ids)
        for topic in topics:
            rcc_detail_pages = rcc_detail_pages.filter(related_topics__topic__translation_key=topic.translation_key)

        return rcc_detail_pages
