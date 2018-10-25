from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from networkapi.buyersguide.models import Product
from networkapi.buyersguide.models import Update


# Wagtail admin
class WagtailBuyersGuideAdmin(ModelAdmin):
    model = Product
    menu_label = 'Buyer\'s Guide'
    menu_icon = 'pick'  # change as required
    menu_order = 600  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', 'company', 'url',)
    search_fields = ('name', 'company')
    index_template_name = 'admin/index_view.html'


class WagtailBuyersGuideUpdateAdmin(ModelAdmin):
    model = Update
    menu_label = 'Updates'
    menu_icon = 'pick'  # change as required
    menu_order = 600  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('source', 'title')
    search_fields = ('source', 'title')


modeladmin_register(WagtailBuyersGuideAdmin)
modeladmin_register(WagtailBuyersGuideUpdateAdmin)
