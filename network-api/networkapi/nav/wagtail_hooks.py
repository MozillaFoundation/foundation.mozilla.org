from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from networkapi.nav.models import NavMenu


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
