from django.contrib import admin

from networkapi.news.models import News
from networkapi.news.forms import NewsAdminForm
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm


admin.site.register(News, NewsAdmin)


class WagtailNewsAdmin(ModelAdmin):
    model = News
    menu_icon = 'doc-full-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('headline', 'thumbnail', 'date', 'link',)
    search_fields = ('headline',)


modeladmin_register(WagtailNewsAdmin)
