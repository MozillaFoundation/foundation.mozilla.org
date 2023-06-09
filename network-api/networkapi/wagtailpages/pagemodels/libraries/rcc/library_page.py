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
from networkapi.wagtailpages.pagemodels.libraries.rcc import (
    constants,
    detail_page,
    taxonomies,
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

    template = "pages/libraries/rcc/library_page.html"

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

    def get_context(self, request: "http.HttpRequest") -> "django_template.Context":
        search_query: str = request.GET.get("search", "")
        sort_value: str = request.GET.get("sort", "")
        sort: constants.SortOption = constants.SORT_CHOICES.get(sort_value, constants.SORT_NEWEST_FIRST)

        filter_form = RCCLibraryPageFilterForm(request.GET, label_suffix="")

        if filter_form.is_valid():
            filtered_author_ids: list[int] = filter_form.cleaned_data["contributors"]
            filtered_content_type_ids: list[int] = filter_form.cleaned_data["content_types"]
            filtered_curricular_area_ids: list[int] = filter_form.cleaned_data["curricular_areas"]
            filtered_topic_ids: list[int] = filter_form.cleaned_data["topics"]
        else:
            # If the form is not valid, we will not filter by any of the values.
            # This will result in all articles being displayed.
            filtered_author_ids = []
            filtered_content_type_ids = []
            filtered_curricular_area_ids = []
            filtered_topic_ids = []

        searched_and_filtered_rcc_detail_pages = self._get_rcc_detail_pages(
            search=search_query,
            sort=sort,
            author_profile_ids=filtered_author_ids,
            content_type_ids=filtered_content_type_ids,
            curricular_area_ids=filtered_curricular_area_ids,
            topic_ids=filtered_topic_ids,
        )

        rcc_detail_pages_paginator = paginator.Paginator(
            object_list=searched_and_filtered_rcc_detail_pages,
            per_page=self.results_count,
            allow_empty_first_page=True,
        )

        page: Optional[str] = request.GET.get("page")
        rcc_detail_pages_page = rcc_detail_pages_paginator.get_page(page)

        context: "django_template.Context" = super().get_context(request)
        context["search_query"] = search_query
        context["sort"] = sort
        context["form"] = filter_form
        context["rcc_detail_pages_count"] = rcc_detail_pages_paginator.count
        context["rcc_detail_pages"] = rcc_detail_pages_page
        return context

    def _get_rcc_detail_pages(
        self,
        *,
        search: str = "",
        sort: constants.SortOption = constants.SORT_NEWEST_FIRST,
        author_profile_ids: Optional[list[int]] = None,
        content_type_ids: Optional[list[int]] = None,
        curricular_area_ids: Optional[list[int]] = None,
        topic_ids: Optional[list[int]] = None,
    ):
        author_profile_ids = author_profile_ids or []
        content_type_ids = content_type_ids or []
        curricular_area_ids = curricular_area_ids or []
        topic_ids = topic_ids or []

        rcc_detail_pages = detail_page.RCCDetailPage.objects.live().public()
        rcc_detail_pages = rcc_detail_pages.filter(locale=wagtail_models.Locale.get_active())

        author_profiles = utils.get_rcc_authors(profile_models.Profile.objects.all())
        author_profiles = author_profiles.filter(id__in=author_profile_ids)
        for author_profile in author_profiles:
            # Synced but not translated pages are still associated with the default
            # locale's author profile. But, we want to show them when we are filtering
            # for the localized author profile. We use the fact that the localized and
            # default locale's author profile have the same `translation_key`.
            rcc_detail_pages = rcc_detail_pages.filter(
                rcc_authors__author_profile__translation_key=(author_profile.translation_key)
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
            rcc_detail_pages = rcc_detail_pages.filter(
                related_topics__rcc_topic__translation_key=topic.translation_key
            )

        rcc_detail_pages = rcc_detail_pages.order_by(sort.order_by_value)

        if search:
            rcc_detail_pages = rcc_detail_pages.search(
                search,
                order_by_relevance=False,  # To preserve original ordering
            )

        return rcc_detail_pages

    def get_banner(self):
        return self.banner_image
