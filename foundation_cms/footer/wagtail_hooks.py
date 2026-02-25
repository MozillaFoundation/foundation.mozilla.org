from wagtail import hooks
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from foundation_cms.footer.models import SiteFooter
from foundation_cms.legacy_apps.wagtailcustomization.views.snippet_chooser import (
    DefaultLocaleSnippetChooserViewSet,
)


@hooks.register("register_icons")
def register_icons(icons):
    return icons + ["icons/footer.svg"]


@hooks.register("register_admin_viewset")
def register_footer_chooser_viewset():
    """
    Custom chooser to only show default locale footers.
    Prevents editors from selecting translations directly.
    """
    return DefaultLocaleSnippetChooserViewSet(
        "wagtailsnippetchoosers_custom_sitefooter",
        model=SiteFooter,
        url_prefix="footer/chooser",
    )


class SiteFooterViewSet(SnippetViewSet):
    model = SiteFooter
    icon = "site"
    menu_order = 200
    menu_label = "Site Footers"
    list_display = ("title",)
    search_fields = ("title",)
    ordering = ("title",)


class SiteFooterViewSetGroup(SnippetViewSetGroup):
    items = (SiteFooterViewSet,)
    menu_label = "Site Footer"
    menu_name = "Site Footer"
    menu_icon = "site"
    add_to_admin_menu = True
    menu_order = 1700


register_snippet(SiteFooterViewSetGroup)
