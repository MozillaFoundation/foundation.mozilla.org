from wagtail import hooks
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from networkapi.nav.models import NavMenu
from networkapi.wagtailcustomization.views.snippet_chooser import (
    DefaultLocaleSnippetChooserViewSet,
)


# Customise chooser to only show the default language nav menus as options.
# We do not want editors to select the translations as
# localisation will be handled on the template instead.
@hooks.register("register_admin_viewset")
def register_nav_menu_chooser_viewset():
    return DefaultLocaleSnippetChooserViewSet(
        "wagtailsnippetchoosers_custom_navmenu",
        model=NavMenu,
        url_prefix="nav/chooser",
    )


class NavMenuViewSet(SnippetViewSet):
    model = NavMenu
    icon = "list-ul"
    menu_order = 100
    menu_label = "Navigation Menus"
    list_display = ("title",)
    search_fields = ("title",)
    ordering = ("title",)


class NavDropdownViewSetGroup(SnippetViewSetGroup):
    items = (NavMenuViewSet,)
    menu_label = "Main Navigation"
    menu_name = "Main Navigation"
    add_to_admin_menu = True
    menu_order = 1600


register_snippet(NavDropdownViewSetGroup)
