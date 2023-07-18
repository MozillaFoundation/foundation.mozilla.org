from django.db.models import Count, Q, Subquery, OuterRef, Max, Prefetch
from wagtail.admin.auth import permission_denied
from wagtail.admin.views.reports import ReportView
from wagtail.models import ContentType, Locale, Page, get_page_models


class PageTypesReportView(ReportView):
    title = "Page Types Report"
    template_name = "pages/reports/page_types_report.html"
    header_icon = "doc-empty-inverse"

    def get_queryset(self):
        default_locale = Locale.get_default()
        page_models = [model.__name__.lower() for model in get_page_models()]
        latest_pages = Prefetch(
            "pages",
            queryset=Page.objects.filter(locale=default_locale).order_by("-latest_revision_created_at"),
            to_attr="last_edited_pages",
        )
        return (
            ContentType.objects.filter(model__in=page_models)
            .annotate(
                count=Count("pages"),
                default_locale_count=Count("pages", filter=Q(pages__locale=default_locale)),
            )
            .prefetch_related(latest_pages)
            .order_by("-count")
        )

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return permission_denied(request)
        return super().dispatch(request, *args, **kwargs)
