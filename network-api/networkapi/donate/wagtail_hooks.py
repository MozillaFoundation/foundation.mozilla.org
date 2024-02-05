from wagtail import hooks
from wagtail.admin.ui.tables import BooleanColumn, UpdatedAtColumn
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from networkapi.donate_banner.models import DonateBanner
from networkapi.wagtailcustomization.views.snippet_chooser import (
    DefaultLocaleSnippetChooserViewSet,
)
from networkapi.wagtailpages.donation_modal import DonationModal


# Customise DonateBanner Snippet admin listing to show extra columns.
class DonateBannerViewSet(SnippetViewSet):
    model = DonateBanner
    icon = "form"  # change as required
    menu_order = 100
    description = "Donation Banner"
    menu_label = "Donation Banners"
    list_display = (
        "name",
        "title",
        BooleanColumn("is_active"),
        UpdatedAtColumn(),
    )
    search_fields = (
        "name",
        "title",
    )
    ordering = ("name",)


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


class DonationModalSnippetViewSet(SnippetViewSet):
    model = DonationModal
    icon = "newspaper"
    menu_order = 200
    menu_label = "Newsletter Signups"
    menu_name = "Newsletter Signups"
    list_display = (
        "name",
        "donate_text",
        "donate_url",
        "dismiss_text",
    )
    search_fields = (
        "name",
        "donate_text",
    )
    ordering = ("name",)


class DonateViewSetGroup(SnippetViewSetGroup):
    items = (
        DonateBannerViewSet,
        DonationModalSnippetViewSet,
    )
    menu_icon = "heart"
    menu_label = "Donate"
    menu_name = "Donate"
    menu_order = 1000


register_snippet(DonateViewSetGroup)
