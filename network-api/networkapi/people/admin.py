from django.contrib import admin
from adminsortable.admin import SortableAdmin

from networkapi.people.models import (
    Person,
    InternetHealthIssue,
    Affiliation,
)
from networkapi.people.forms import PersonAdminForm
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)


class AffiliationAdmin(admin.TabularInline):
    model = Affiliation
    extra = 1
    verbose_name_plural = """Affiliations  (e.g. companies, nonprofits, universities, projects and
    other organizations this person is actively involved with)"""


class PersonAdmin(SortableAdmin):
    form = PersonAdminForm
    inlines = [
        AffiliationAdmin,
    ]
    sortable_change_list_template = (
        'shared/adminsortable_change_list_custom.html',
    )

    class Media:
        js = ('/static/people/js/admin.js',)


admin.site.register(Person, PersonAdmin)
admin.site.register(InternetHealthIssue)


# Wagtail admin
class WagtailPersonAdmin(ModelAdmin):
    model = Person
    menu_icon = 'user'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = True  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', 'role', 'location')
    list_filter = ('internet_health_issues',)
    search_fields = ('name')


modeladmin_register(WagtailPersonAdmin)
