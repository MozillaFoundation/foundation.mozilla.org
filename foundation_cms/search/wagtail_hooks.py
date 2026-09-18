from django.db.models import Count, IntegerField, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.admin.menu import AdminOnlyMenuItem
from wagtail.admin.ui.tables import NumberColumn
from wagtail.contrib.search_promotions.views.reports import SearchTermsReportView

from foundation_cms.search.models import SearchEvent


class SearchTermsWithEngagementReportView(SearchTermsReportView):
    """
    Extends the default search terms report to include engagement metrics.
    Adds a secondary "refinements" column, separate from raw search hits.
    """

    columns = SearchTermsReportView.columns + [
        NumberColumn("_refinements", label=_("Sort/Filter Refinements"), sort_key="_refinements"),
    ]
    export_headings = {**SearchTermsReportView.export_headings, "_refinements": _("Sort/Filter Refinements")}
    list_export = SearchTermsReportView.list_export + ["_refinements"]
    index_url_name = "foundation_search_terms_report"
    index_results_url_name = "foundation_search_terms_report_results"

    def get_base_queryset(self):
        refinement_counts = (
            SearchEvent.objects.filter(query_string=OuterRef("query_string"), is_refinement=True)
            .order_by()
            .values("query_string")
            .annotate(count=Count("id"))
            .values("count")
        )
        return (
            super()
            .get_base_queryset()
            .annotate(_refinements=Coalesce(Subquery(refinement_counts, output_field=IntegerField()), 0))
        )


@hooks.register("register_admin_urls")
def register_search_terms_report_urls():
    return [
        path(
            "reports/search-terms-engagement/",
            SearchTermsWithEngagementReportView.as_view(),
            name="foundation_search_terms_report",
        ),
        path(
            "reports/search-terms-engagement/results/",
            SearchTermsWithEngagementReportView.as_view(results_only=True),
            name="foundation_search_terms_report_results",
        ),
    ]


@hooks.register("construct_reports_menu")
def hide_default_search_terms_menu_item(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name != "search-terms"]


@hooks.register("register_reports_menu_item")
def register_search_terms_report_menu_item():
    return AdminOnlyMenuItem(
        _("Search terms"),
        reverse("foundation_search_terms_report"),
        name="search-terms-engagement",
        icon_name="search",
        order=1300,
    )
