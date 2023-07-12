from django.db.models import Count
from wagtail.admin.auth import permission_denied
from wagtail.admin.views.reports import ReportView
from wagtail.models import ContentType


class PageTypesReportView(ReportView):
    title = "Page Types Report"
    template_name = "pages/reports/page_types_report.html"
    header_icon = "doc-empty-inverse"

    def get_queryset(self):
        return ContentType.objects.filter(model__iendswith="page").annotate(count=Count("pages")).order_by("-count")

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return permission_denied(request)
        return super().dispatch(request, *args, **kwargs)
