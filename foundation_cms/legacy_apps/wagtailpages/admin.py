from taggit.models import Tag
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet


# Wagtail admin
class WagtailTagSnippetViewSet(SnippetViewSet):
    model = Tag
    icon = "tag"
    menu_label = "Tags"
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True
    exclude_from_explorer = True
    list_display = ("name",)
    search_fields = ("name",)


register_snippet(WagtailTagSnippetViewSet)
