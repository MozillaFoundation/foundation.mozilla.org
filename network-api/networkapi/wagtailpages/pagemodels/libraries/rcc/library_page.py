import typing
from typing import Optional

from django.core import paginator
from django.db import models
from wagtail import images as wagtail_images
from wagtail import models as wagtail_models
from wagtail.admin import panels
from wagtail.images import edit_handlers as image_panels
from wagtail_localize.fields import SynchronizedField, TranslatableField

from networkapi.wagtailpages import utils
from networkapi.wagtailpages.pagemodels import profiles as profile_models
from networkapi.wagtailpages.pagemodels.base import BasePage
from networkapi.wagtailpages.pagemodels.libraries.rcc import (  # taxonomies,
    constants,
    detail_page,
)
from networkapi.wagtailpages.pagemodels.libraries.rcc.forms import (
    RCCLibraryPageFilterForm,
)

if typing.TYPE_CHECKING:
    from django import http
    from django import template as django_template


class RCCLibraryPage(BasePage):
    max_count = 1

    parent_page_types = ["RCCLandingPage"]

    subpage_types = ["RCCDetailPage"]

    template = "pages/rcc/library_page.html"

    SORT_CHOICES = constants.SORT_CHOICES

    banner_image = models.ForeignKey(
        wagtail_images.get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    results_count = models.PositiveSmallIntegerField(
        default=10,
        help_text="Maximum number of results to be displayed per page.",
    )

    content_panels = BasePage.content_panels + [
        image_panels.FieldPanel("banner_image"),
    ]

    settings_panels = BasePage.settings_panels + [panels.FieldPanel("results_count")]

    translatable_fields = [
        # Content tab fields
        TranslatableField("title"),
        # Promote tab fields
        SynchronizedField("slug"),
        TranslatableField("seo_title"),
        SynchronizedField("show_in_menus"),
        TranslatableField("search_description"),
        SynchronizedField("search_image"),
    ]

    # def get_context(self, request: "http.HttpRequest") -> "django_template.Context":
    #     search_query: str = request.GET.get("search", "")
    #     sort_value: str = request.GET.get("sort", "")
    #     sort: constants.SortOption = constants.SORT_CHOICES.get(sort_value, constants.SORT_NEWEST_FIRST)

    #     filter_form = LibraryPageFilterForm(request.GET, label_suffix="")
    #     if not filter_form.is_valid():
    #         # If the form is not valid, we will not filter by any of the values.
    #         # This will result in all research being displayed.
    #         filtered_author_ids: list[int] = []
    #         filtered_topic_ids: list[int] = []
    #         filtered_region_ids: list[int] = []
    #         filtered_year: Optional[int] = None

    #     filtered_author_ids = filter_form.cleaned_data["author"]
    #     filtered_topic_ids = filter_form.cleaned_data["topic"]
    #     filtered_region_ids = filter_form.cleaned_data["region"]
    #     filtered_year = filter_form.cleaned_data["year"]

    #     searched_and_filtered_research_detail_pages = self._get_research_detail_pages(
    #         search=search_query,
    #         sort=sort,
    #         author_profile_ids=filtered_author_ids,
    #         topic_ids=filtered_topic_ids,
    #         region_ids=filtered_region_ids,
    #         year=filtered_year,
    #     )
    #     research_detail_pages_paginator = paginator.Paginator(
    #         object_list=searched_and_filtered_research_detail_pages,
    #         per_page=self.results_count,
    #         allow_empty_first_page=True,
    #     )

    #     page: Optional[str] = request.GET.get("page")
    #     research_detail_pages_page = research_detail_pages_paginator.get_page(page)

    #     context: "django_template.Context" = super().get_context(request)
    #     context["search_query"] = search_query
    #     context["sort"] = sort
    #     context["form"] = filter_form
    #     context["research_detail_pages_count"] = research_detail_pages_paginator.count
    #     context["research_detail_pages"] = research_detail_pages_page
    #     return context

    # def _get_research_detail_pages(
    #     self,
    #     *,
    #     search: str = "",
    #     sort: constants.SortOption = constants.SORT_NEWEST_FIRST,
    #     author_profile_ids: Optional[list[int]] = None,
    #     topic_ids: Optional[list[int]] = None,
    #     region_ids: Optional[list[int]] = None,
    #     year: Optional[int] = None,
    # ):
    #     author_profile_ids = author_profile_ids or []
    #     topic_ids = topic_ids or []
    #     region_ids = region_ids or []

    #     research_detail_pages = detail_page.ResearchDetailPage.objects.live().public()
    #     research_detail_pages = research_detail_pages.filter(locale=wagtail_models.Locale.get_active())

    #     author_profiles = utils.get_research_authors(profile_models.Profile.objects.all())
    #     author_profiles = author_profiles.filter(id__in=author_profile_ids)
    #     for author_profile in author_profiles:
    #         # Synced but not translated pages are still associated with the default
    #         # locale's author profile. But, we want to show them when we are filtering
    #         # for the localized author profile. We use the fact that the localized and
    #         # default locale's author profile have the same `translation_key`.
    #         research_detail_pages = research_detail_pages.filter(
    #             research_authors__author_profile__translation_key=(author_profile.translation_key)
    #         )

    #     topics = taxonomies.ResearchTopic.objects.filter(id__in=topic_ids)
    #     for topic in topics:
    #         research_detail_pages = research_detail_pages.filter(
    #             related_topics__research_topic__translation_key=topic.translation_key
    #         )

    #     regions = taxonomies.ResearchRegion.objects.filter(id__in=region_ids)
    #     for region in regions:
    #         research_detail_pages = research_detail_pages.filter(
    #             related_regions__research_region__translation_key=region.translation_key
    #         )

    #     if year:
    #         research_detail_pages = research_detail_pages.filter(original_publication_date__year=year)

    #     research_detail_pages = research_detail_pages.order_by(sort.order_by_value)

    #     if search:
    #         research_detail_pages = research_detail_pages.search(
    #             search,
    #             order_by_relevance=False,  # To preserve original ordering
    #         )

    #     return research_detail_pages

    def get_banner(self):
        return self.banner_image
