from collections import defaultdict

import django_filters
from django.contrib.auth import get_user_model
from django.db.models import BooleanField, Case, Count, OuterRef, Q, Subquery, When
from wagtail.admin.filters import WagtailFilterSet
from wagtail.admin.views.reports import ReportView
from wagtail.coreutils import get_content_languages
from wagtail.models import ContentType, Page, PageLogEntry, get_page_models
from wagtail.users.utils import get_deleted_user_display_name
from wagtailinventory.models import PageBlock


def _get_locale_choices():
    choices = [(language_code, display_name) for language_code, display_name in get_content_languages().items()]
    return choices


class LocaleFilter(django_filters.ChoiceFilter):
    def filter(self, qs, value):
        if value and value != self.null_value:
            latest_edit_log = PageLogEntry.objects.filter(
                content_type=OuterRef("pk"), page__locale__language_code=value
            )
            count_qs = Count("pages", filter=Q(pages__locale__language_code=value))
        else:
            latest_edit_log = PageLogEntry.objects.filter(content_type=OuterRef("pk"))
            count_qs = Count("pages")

        latest_edit_log = latest_edit_log.order_by("-timestamp", "-pk")

        qs = qs.annotate(
            count=count_qs,
            last_edited_page=Subquery(latest_edit_log.values("page")[:1]),
            last_edited_by=Subquery(latest_edit_log.values("user")[:1]),
        )

        return qs


class PageTypesReportFilterSet(WagtailFilterSet):
    page_locale = LocaleFilter(
        label="Locale", choices=_get_locale_choices, empty_label=None, null_label="All", null_value="all"
    )

    class Meta:
        model = ContentType
        fields = ["page_locale"]


class PageTypesReportView(ReportView):
    title = "Page types report"
    template_name = "pages/reports/page_types_report.html"
    header_icon = "doc-empty-inverse"

    filterset_class = PageTypesReportFilterSet

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_model = get_user_model()
        self.page_models = [model.__name__.lower() for model in get_page_models()]

    def add_last_edited_name_to_page_type(self, username_mapping, page_type):
        if page_type.last_edited_by:
            last_edited_by_user = username_mapping.get(
                page_type.last_edited_by, get_deleted_user_display_name(user_id=page_type.last_edited_by)
            )
            page_type.last_edited_by_user = last_edited_by_user

    def add_last_edited_page_to_page_type(self, pages_mapping, page_type):
        if page_type.last_edited_page:
            last_edited_page = pages_mapping.get(page_type.last_edited_page, None)
            page_type.last_edited_page = last_edited_page

    def decorate_paginated_queryset(self, page_types):
        page_ids = set(page_types.values_list("last_edited_page", flat=True))
        pages_mapping = {page.pk: page for page in Page.objects.filter(pk__in=page_ids)}

        user_ids = set(page_types.values_list("last_edited_by", flat=True))
        username_mapping = {user.pk: user.get_username() for user in self.user_model.objects.filter(pk__in=user_ids)}

        for page_type in page_types:
            self.add_last_edited_page_to_page_type(pages_mapping, page_type)
            self.add_last_edited_name_to_page_type(username_mapping, page_type)
        return page_types

    def get_queryset(self):
        queryset = ContentType.objects.filter(model__in=self.page_models)
        self.queryset = queryset

        queryset = self.filter_queryset(queryset)

        # 'updated_at' is handled at the filter level, since ContentType itself does not
        # have a locale to filter on

        queryset = queryset.order_by("-count", "app_label", "model")

        return queryset


class BlockTypesReportView(ReportView):
    title = "Block types report"
    template_name = "pages/reports/block_types_report.html"
    header_icon = "placeholder"

    def decorate_paginated_queryset(self, object_list):
        # Build a cache map of PageBlock's block name to content types
        page_blocks = PageBlock.objects.all().prefetch_related("page__content_type")
        blocks_to_content_types = defaultdict(list)
        for page_block in page_blocks:
            if page_block.page.live and (
                page_block.page.content_type not in blocks_to_content_types[page_block.block]
            ):
                blocks_to_content_types[page_block.block].append(page_block.page.content_type)

        # Get the content_types for each block name
        for block_report_item in object_list:
            content_types = blocks_to_content_types.get(block_report_item["block"], [])
            block_report_item["content_types"] = content_types
            block_report_item["type_label"] = "Custom" if block_report_item["is_custom_block"] else "Core"

        return object_list

    def get_queryset(self):
        queryset = (
            PageBlock.objects.all()
            .values("block")
            .annotate(
                count=Count("page", filter=Q(page__live=True)),
                is_custom_block=Case(
                    When(block__startswith="wagtail.", then=False), default=True, output_field=BooleanField()
                ),
            )
        )
        self.queryset = queryset

        queryset = queryset.order_by("-count", "block")

        return queryset
