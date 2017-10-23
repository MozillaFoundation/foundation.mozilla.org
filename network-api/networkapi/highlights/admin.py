from django.contrib import admin
from adminsortable.admin import SortableAdmin

from networkapi.highlights.models import Highlight
from networkapi.highlights.forms import HighlightAdminForm


class HighlightAdmin(SortableAdmin):
    form = HighlightAdminForm

    sortable_change_list_template = (
        'shared/adminsortable_change_list_custom.html',
    )

admin.site.register(Highlight, HighlightAdmin)
