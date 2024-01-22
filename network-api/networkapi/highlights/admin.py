from adminsortable.admin import SortableAdmin
from django.contrib import admin
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from networkapi.highlights.forms import HighlightAdminForm
from networkapi.highlights.models import Highlight


@admin.register(Highlight)
class HighlightAdmin(SortableAdmin):
    form = HighlightAdminForm

    sortable_change_list_template = ("shared/adminsortable_change_list_custom.html",)


# Wagtail admin
class WagtailHighlightSnippetViewSet(SnippetViewSet):
    model = Highlight
    icon = "date"  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    add_to_admin_menu = True  # or True to hide it from the Wagtail side menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = (
        "title",
        "description",
        "link_url",
    )
    search_fields = ("title", "description")


register_snippet(WagtailHighlightSnippetViewSet)
