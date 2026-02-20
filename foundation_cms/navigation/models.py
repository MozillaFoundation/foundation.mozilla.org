from django.db import models
from django.utils.functional import cached_property
from modelcluster.models import ClusterableModel
from wagtail import models as wagtail_models
from wagtail.admin import panels
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField
from wagtail.search import index
from wagtail_localize.fields import SynchronizedField, TranslatableField

from foundation_cms.legacy_apps.nav import blocks as nav_blocks
from foundation_cms.legacy_apps.nav import utils as nav_utils
from foundation_cms.legacy_apps.nav.forms import NavMenuForm


class NavMenu(
    wagtail_models.PreviewableMixin,
    wagtail_models.DraftStateMixin,
    wagtail_models.RevisionMixin,
    wagtail_models.TranslatableMixin,
    ClusterableModel,
):
    title = models.CharField(max_length=100, help_text="For internal identification only")

    dropdowns = StreamField(
        [
            ("dropdown", nav_blocks.NavDropdown(label="Dropdown")),
        ],
        use_json_field=True,
        min_num=1,
        max_num=5,
        help_text="Add up to 5 dropdown menus",
    )

    panels = [
        panels.HelpPanel(content="To enable a navigation menu on a site, go to Settings > Navigation Menus."),
        panels.FieldPanel("title"),
        panels.FieldPanel("dropdowns"),
    ]
    base_form_class = NavMenuForm

    translatable_fields = [
        SynchronizedField("title"),
        TranslatableField("dropdowns"),
    ]

    search_fields = [
        index.SearchField("title"),
    ]

    class Meta(wagtail_models.TranslatableMixin.Meta):
        verbose_name = "Navigation Menu"
        verbose_name_plural = "Navigation Menus"

    def __str__(self) -> str:
        return self.title

    def get_preview_template(self, request, mode_name):
        return "previews/nav/menu.html"

    def get_preview_context(self, request, mode_name):
        context = super().get_preview_context(request, mode_name)
        return context

    @cached_property
    def page_references_per_dropdown(self):
        """
        Get CMS page paths per dropdown id.

        Structure:
        {
          "<dropdown_stream_id>": {
              "page_ids": [<ids referenced anywhere in the dropdown>],
              "self_page_id": <header page id if header links to a page else None>,
              <page_id>: <page.path>,
              ...
          },
          ...
        }
        """
        dropdown_page_links: dict[str, dict] = {}

        for dropdown in self.dropdowns.raw_data:
            # Find all referenced page IDs inside this dropdown (header + items)
            local_page_ids = list(nav_utils.find_key_values(dropdown, "page"))
            local_page_ids = [pid for pid in local_page_ids if pid]  # filter out empty values

            dropdown_page_links[dropdown["id"]] = {"page_ids": local_page_ids, "self_page_id": None}

            # "Dropdown itself should be a link": treat header page as "self" when it's a page link
            value = dropdown.get("value") or {}
            header = value.get("header") or {}
            header_link_to = header.get("link_to")
            header_page_id = header.get("page")

            if header_link_to == "page" and header_page_id:
                dropdown_page_links[dropdown["id"]]["self_page_id"] = header_page_id

        # Flat list of all page ids referenced across all dropdowns
        page_ids: list[int] = []
        for d in dropdown_page_links.values():
            page_ids.extend(d["page_ids"])

        # Fetch all paths for referenced pages
        paths_qs = wagtail_models.Page.objects.filter(id__in=page_ids).values("id", "path")
        paths = {p["id"]: p["path"] for p in paths_qs}

        # Map paths back onto each dropdown bucket (same pattern you had before)
        for d in dropdown_page_links.values():
            for pid in d["page_ids"]:
                # Only map if found (defensive against stale ids)
                if pid in paths:
                    d[pid] = paths[pid]

        return dropdown_page_links

    @cached_property
    def page_references(self):
        """
        Get all CMS page paths referenced anywhere in the dropdowns.
        Returns: {<page_id>: <page.path>, ...}
        """
        page_ids: list[int] = []
        for dropdown in self.dropdowns.raw_data:
            page_ids.extend(list(nav_utils.find_key_values(dropdown, "page")))

        page_ids = [pid for pid in page_ids if pid]  # filter out empty values

        paths_qs = wagtail_models.Page.objects.filter(id__in=page_ids).values("id", "path")
        return {p["id"]: p["path"] for p in paths_qs}


@register_setting(icon="nav-menu")
class SiteNavMenu(BaseSiteSetting):
    select_related = ["active_nav_menu"]

    active_nav_menu = models.ForeignKey(
        "nav.NavMenu",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="site_nav_menu",
        verbose_name="Active Navigation Menu",
    )

    content_panels = [
        panels.FieldPanel("active_nav_menu"),
    ]

    class Meta:
        verbose_name = "Navigation Menu"
        verbose_name_plural = "Navigation Menus"