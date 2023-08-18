from django.contrib.auth import get_user_model
from django.db.models import Count, OuterRef, Q, Subquery
from django.utils import translation
from wagtail.admin.views.reports import ReportView
from wagtail.models import ContentType, Locale, Page, PageLogEntry, get_page_models
from wagtail.users.utils import get_deleted_user_display_name


class PageTypesReportView(ReportView):
    title = "Page Types Report"
    template_name = "pages/reports/page_types_report.html"
    header_icon = "doc-empty-inverse"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_model = get_user_model()
        self.default_locale = Locale.get_default()
        self.active_locale = Locale.get_active()
        self.active_locale_name = translation.get_language_info(self.active_locale.language_code)["name_local"]

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
        page_models = [model.__name__.lower() for model in get_page_models()]

        latest_edit_log = PageLogEntry.objects.filter(
            content_type=OuterRef("pk"), page__locale=self.active_locale
        ).order_by("-timestamp")

        return (
            ContentType.objects.filter(model__in=page_models)
            .annotate(
                count=Count("pages"),
                active_locale_count=Count("pages", filter=Q(pages__locale=self.active_locale)),
                last_edited_page=Subquery(latest_edit_log.values("page")[:1]),
                last_edited_by=Subquery(latest_edit_log.values("user")[:1]),
            )
            .order_by("-count")
        )
