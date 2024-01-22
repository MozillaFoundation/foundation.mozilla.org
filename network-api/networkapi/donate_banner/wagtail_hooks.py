from django.db import models
from wagtail import hooks
from wagtail.admin.panels import FieldPanel
from wagtail.admin.ui.tables import UpdatedAtColumn
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from networkapi.donate_banner.models import DonateBanner
from networkapi.wagtailcustomization.views.snippet_chooser import (
    DefaultLocaleSnippetChooserViewSet,
)


# Customise DonateBanner Snippet admin listing to show extra columns.
class DonateBannerViewSet(SnippetViewSet):
    model = DonateBanner
    icon = "form"  # change as required
    menu_order = 1100
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    add_to_admin_menu = True
    exclude_from_explorer = False
    description = "Donation Banner"
    menu_label = "Donation Banners"
    list_display = ["name", "cta_link", "is_active", UpdatedAtColumn()]


register_snippet(DonateBanner, viewset=DonateBannerViewSet)


# Customise chooser to only show the default language banners as options.
# We do not want editors to select the translations as
# localisation will be handled on the template instead.
@hooks.register("register_admin_viewset")
def register_donate_banner_chooser_viewset():
    return DefaultLocaleSnippetChooserViewSet(
        "wagtailsnippetchoosers_custom_donatebanner",
        model=DonateBanner,
        url_prefix="donate_banner/chooser",
    )


@register_setting(icon="pick")
class SiteDonateBanner(BaseSiteSetting):
    select_related = ["active_donate_banner"]

    active_donate_banner = models.ForeignKey(
        "donate_banner.DonateBanner",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="site_donate_banner",
    )

    content_panels = [
        FieldPanel("active_donate_banner"),
    ]

    class Meta:
        verbose_name = "Donate Banner"
