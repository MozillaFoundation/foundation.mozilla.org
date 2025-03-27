import typing
from functools import cached_property
from typing import Optional

from django.core import paginator
from django.db import models
from wagtail import images as wagtail_images
from wagtail.admin import panels
from wagtail_localize.fields import SynchronizedField, TranslatableField
from wagtail.images import get_image_model_string

from networkapi.wagtailpages.pagemodels.base import BasePage
from networkapi.wagtailpages.pagemodels.libraries import constants

if typing.TYPE_CHECKING:
    from django import forms, http
    from django import template as django_template
    from django.db.models.query import QuerySet


class BaseLibraryPage(BasePage):
    """An abstract template for a library page.

    To define a concrete library page, subclass it and implement the following attributes:
    - `parent_page_types`: Return the parent page types for this page.
    - `subpage_types`: Return the subpage types for this page.
    - `template`: Return the template to use for this page.

    In addition, the following methods have to be implemented:
    - `get_form`: Return the form class used to filter detail pages.
    - `get_filtered_detail_pages`: Return the article detail pages that match the given filters in the form.

    Concrete implementation examples can be found in the RCC and Research_Hub apps.
    """

    max_count = 1

    template = "pages/libraries/library_page.html"

    SORT_CHOICES = constants.SORT_CHOICES

    banner_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    results_count = models.PositiveSmallIntegerField(
        default=10,
        help_text="Maximum number of results to be displayed per page.",
    )

    content_panels = BasePage.content_panels + [
        panels.FieldPanel("banner_image"),
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

    class Meta:
        abstract = True

    @property
    def filter_form(self):
        """Form class used to filter detail pages for this page."""
        raise NotImplementedError("Please implement this property in your subclass.")

    @cached_property
    def detail_pages(self):
        """Return the article detail pages that are children of this page."""
        raise NotImplementedError("Please implement this property in your subclass.")

    @staticmethod
    def filter_detail_pages(pages: "QuerySet", filter_form: "forms.Form") -> "QuerySet":
        """Return the article detail pages that match the given filters in the `filter_form`."""
        raise NotImplementedError("Please implement this method in your subclass.")

    def get_sorted_filtered_detail_pages(
        self,
        *,
        filter_form: Optional["forms.Form"] = None,
        sort: constants.SortOption = constants.SORT_NEWEST_FIRST,
        search_query: Optional[str] = None,
    ) -> "QuerySet":
        """Get sorted article detail pages filtered by the form options and search parameters."""
        detail_pages = self.detail_pages

        if filter_form:
            detail_pages = self.filter_detail_pages(detail_pages, filter_form)

        detail_pages = detail_pages.order_by(sort.order_by_value)

        if search_query:
            detail_pages = detail_pages.search(
                search_query,
                order_by_relevance=False,  # To preserve original ordering
            )

        return detail_pages

    def get_context(self, request: "http.HttpRequest") -> "django_template.Context":
        search_query: str = request.GET.get("search", "")
        sort_value: str = request.GET.get("sort", "")
        sort: constants.SortOption = constants.SORT_CHOICES.get(sort_value, constants.SORT_NEWEST_FIRST)

        Form = self.filter_form
        filter_form = Form(request.GET, label_suffix="")

        sorted_and_searched_and_filtered_detail_pages = self.get_sorted_filtered_detail_pages(
            filter_form=filter_form, search_query=search_query, sort=sort
        )

        detail_pages_paginator = paginator.Paginator(
            object_list=sorted_and_searched_and_filtered_detail_pages,
            per_page=self.results_count,
            allow_empty_first_page=True,
        )

        page: Optional[str] = request.GET.get("page")
        detail_pages_page = detail_pages_paginator.get_page(page)

        context: "django_template.Context" = super().get_context(request)
        context["search_query"] = search_query
        context["sort"] = sort
        context["form"] = filter_form
        context["detail_pages_count"] = detail_pages_paginator.count
        context["detail_pages"] = detail_pages_page
        return context

    def get_banner(self):
        return self.banner_image
