from wagtail import hooks
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from foundation_cms.navigation.models import NavigationMenu
from foundation_cms.legacy_apps.wagtailcustomization.views.snippet_chooser import (
    DefaultLocaleSnippetChooserViewSet,
)


@hooks.register("register_icons")
def register_icons(icons):
    return icons + ["icons/nav-dropdown.svg", "icons/nav-menu.svg"]


# Customise chooser to only show the default language nav menus as options.
# We do not want editors to select the translations as
# localisation will be handled on the template instead.
@hooks.register("register_admin_viewset")
def register_nav_menu_chooser_viewset():
    return DefaultLocaleSnippetChooserViewSet(
        "wagtailsnippetchoosers_custom_navigationmenu",
        model=NavigationMenu,
        url_prefix="navigation/chooser",
    )


class NavigationMenuViewSet(SnippetViewSet):
    model = NavigationMenu
    icon = "nav-menu"
    menu_order = 100
    menu_label = "Navigation Menus"
    list_display = ("title",)
    search_fields = ("title",)
    ordering = ("title",)


class NavigationMenuViewSetGroup(SnippetViewSetGroup):
    items = (NavigationMenuViewSet,)
    menu_label = "Main Navigation"
    menu_name = "Main Navigation"
    menu_icon = "nav-menu"
    add_to_admin_menu = True
    menu_order = 100

register_snippet(NavigationMenuViewSetGroup)
