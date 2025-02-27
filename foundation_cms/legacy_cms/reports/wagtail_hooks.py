from django.urls import path, reverse
from wagtail import hooks
from wagtail.admin.menu import AdminOnlyMenuItem

from .views import BlockTypesReportView, PageTypesReportView


@hooks.register("register_reports_menu_item")
def register_page_types_report_menu_item():
    return AdminOnlyMenuItem(
        "Page types", reverse("page_types_report"), icon_name=PageTypesReportView.header_icon, order=700
    )


@hooks.register("register_admin_urls")
def register_page_types_report_url():
    return [
        path("reports/page-types-report/", PageTypesReportView.as_view(), name="page_types_report"),
    ]


@hooks.register("register_reports_menu_item")
def register_block_types_report_menu_item():
    return AdminOnlyMenuItem(
        "Block types", reverse("block_types_report"), icon_name=BlockTypesReportView.header_icon, order=701
    )


@hooks.register("register_admin_urls")
def register_block_types_report_url():
    return [
        path("reports/block-types-report/", BlockTypesReportView.as_view(), name="block_types_report"),
    ]
