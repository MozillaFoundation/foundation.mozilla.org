from django.contrib import admin
from adminsortable.admin import SortableAdmin

from networkapi.highlights.models import Highlight
from networkapi.highlights.forms import HighlightAdminForm
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)


class HighlightAdmin(SortableAdmin):
    form = HighlightAdminForm

    sortable_change_list_template = (
        'shared/adminsortable_change_list_custom.html',
    )


admin.site.register(Highlight, HighlightAdmin)


# Wagtail admin
class WagtailHighlightAdmin(ModelAdmin):
    model = Highlight
    menu_icon = 'date'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('title', 'description', 'link_url',)
    search_fields = ('title', 'description')


modeladmin_register(WagtailHighlightAdmin)
