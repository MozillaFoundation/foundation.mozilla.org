from django.contrib import admin
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from networkapi.news.forms import NewsAdminForm
from networkapi.news.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm


class WagtailNewsSnippetViewSet(SnippetViewSet):
    model = News
    icon = "doc-full-inverse"  # change as required
    menu_order = 201  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    add_to_admin_menu = True  # or True to hide it from the Wagtail side menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = (
        "headline",
        "thumbnail",
        "date",
        "link",
    )
    search_fields = ("headline",)


register_snippet(WagtailNewsSnippetViewSet)
