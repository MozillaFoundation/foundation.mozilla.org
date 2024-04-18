from django.db import models
from wagtail import models as wagtail_models
from wagtail.admin import panels
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField
from wagtail.search import index
from wagtail_localize.fields import TranslatableField

from networkapi.nav import blocks as nav_blocks


class NavMenu(
    wagtail_models.PreviewableMixin,
    wagtail_models.DraftStateMixin,
    wagtail_models.RevisionMixin,
    wagtail_models.TranslatableMixin,
    models.Model,
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

    translatable_fields = [
        TranslatableField("title"),
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


@register_setting
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
