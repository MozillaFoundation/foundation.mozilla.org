import typing
from functools import cached_property
from typing import Optional

from wagtail import models as wagtail_models

from legacy_cms.wagtailpages.pagemodels.libraries import (
    library_page as base_library_page,
)
from legacy_cms.wagtailpages.pagemodels.libraries.research_hub import (
    detail_page,
    taxonomies,
)
from legacy_cms.wagtailpages.pagemodels.libraries.research_hub import (
    utils as research_utils,
)
from legacy_cms.wagtailpages.pagemodels.libraries.research_hub.forms import (
    ResearchLibraryPageFilterForm,
)

if typing.TYPE_CHECKING:
    from django import forms
    from django.db.models.query import QuerySet


class ResearchLibraryPage(base_library_page.BaseLibraryPage):
    parent_page_types = ["ResearchLandingPage"]

    subpage_types = ["ResearchDetailPage"]

    template = "pages/libraries/research_hub/library_page.html"

    @property
    def filter_form(self) -> "forms.Form":
        """Form class used to filter detail pages for this page."""
        return ResearchLibraryPageFilterForm

    @cached_property
    def detail_pages(self) -> "QuerySet[detail_page.ResearchDetailPage]":
        """Return the article detail pages that are children of this page."""
        return detail_page.ResearchDetailPage.objects.live().public().filter(locale=wagtail_models.Locale.get_active())

    @staticmethod
    def filter_detail_pages(
        pages: "QuerySet[detail_page.ResearchDetailPage]", filter_form: "forms.Form"
    ) -> "QuerySet[detail_page.ResearchDetailPage]":
        """Return the article detail pages that match the given filters in the form."""
        if filter_form.is_valid():
            author_profile_ids: list[int] = filter_form.cleaned_data["authors"]
            topic_ids: list[int] = filter_form.cleaned_data["topics"]
            region_ids: list[int] = filter_form.cleaned_data["regions"]
            year: Optional[int] = filter_form.cleaned_data["year"]
        else:
            # If the form is not valid, we will not filter by any of the values.
            # This will result in all research being displayed.
            author_profile_ids = []
            topic_ids = []
            region_ids = []
            year = None

        research_detail_pages = pages

        author_profiles = research_utils.get_research_authors()
        author_profiles = author_profiles.filter(id__in=author_profile_ids)
        for author_profile in author_profiles:
            # Synced but not translated pages are still associated with the default
            # locale's author profile. But, we want to show them when we are filtering
            # for the localized author profile. We use the fact that the localized and
            # default locale's author profile have the same `translation_key`.
            research_detail_pages = research_detail_pages.filter(
                authors__author_profile__translation_key=(author_profile.translation_key)
            )

        topics = taxonomies.ResearchTopic.objects.filter(id__in=topic_ids)
        for topic in topics:
            research_detail_pages = research_detail_pages.filter(
                related_topics__topic__translation_key=topic.translation_key
            )

        regions = taxonomies.ResearchRegion.objects.filter(id__in=region_ids)
        for region in regions:
            research_detail_pages = research_detail_pages.filter(
                related_regions__region__translation_key=region.translation_key
            )

        if year:
            research_detail_pages = research_detail_pages.filter(original_publication_date__year=year)

        return research_detail_pages
