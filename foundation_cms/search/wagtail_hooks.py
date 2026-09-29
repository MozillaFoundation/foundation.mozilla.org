from django.db.models import Count, IntegerField, OuterRef, Subquery, Sum
from django.db.models.functions import Coalesce
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.admin.menu import AdminOnlyMenuItem
from wagtail.admin.ui.tables import NumberColumn
from wagtail.contrib.search_promotions.models import Query, QueryDailyHits
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
        queryset = Query.objects.filter(daily_hits__isnull=False).distinct()
        return self._annotate_counts(queryset, date_range=None)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        date_range = self.filters.form.cleaned_data.get("hit_date") if self.filters else None

        if not date_range:
            return queryset

        return self._annotate_counts(queryset, date_range)

    def _annotate_counts(self, queryset, date_range):
        return queryset.annotate(
            _hits=Coalesce(Subquery(self._hits_subquery(date_range), output_field=IntegerField()), 0),
            _refinements=Coalesce(Subquery(self._refinements_subquery(date_range), output_field=IntegerField()), 0),
        )

    def _hits_subquery(self, date_range):
        hits = self._restrict_to_date_range(QueryDailyHits.objects.filter(query_id=OuterRef("pk")), date_range, "date")
        return hits.order_by().values("query_id").annotate(total=Sum("hits")).values("total")

    def _refinements_subquery(self, date_range):
        refinements = self._restrict_to_date_range(
            SearchEvent.objects.filter(query_string=OuterRef("query_string"), is_refinement=True),
            date_range,
            "created_at__date",
        )
        return refinements.order_by().values("query_string").annotate(count=Count("id")).values("count")

    @staticmethod
    def _restrict_to_date_range(queryset, date_range, date_field):
        """
        Restrict the given queryset to the specified date range.

        Args:
            queryset: The initial queryset to filter.
            date_range: An object with 'start' and 'stop' attributes representing the date range.
            date_field: The name of the date field to filter on.

        Returns:
            The filtered queryset.
        """
        if not date_range:
            return queryset
        if date_range.start:
            queryset = queryset.filter(**{f"{date_field}__gte": date_range.start})
        if date_range.stop:
            queryset = queryset.filter(**{f"{date_field}__lte": date_range.stop})

        return queryset


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
