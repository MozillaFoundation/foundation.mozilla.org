from taggit.models import Tag
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)


# Wagtail admin
class WagtailTagAdmin(ModelAdmin):
    model = Tag
    menu_label = 'Tags'
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True
    exclude_from_explorer = True
    list_display = ('name', )
    search_fields = ('name', )


modeladmin_register(WagtailTagAdmin)
