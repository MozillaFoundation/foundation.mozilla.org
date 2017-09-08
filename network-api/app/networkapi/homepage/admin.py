from django.contrib import admin
from mezzanine.utils.admin import SingletonAdmin

from networkapi.homepage.models import (
    Homepage,
    HomepageLeaders,
    HomepageNews,
    HomepageHighlights,
)


# Base class for the inline forms for People, News, and Highlights
# containing the common config for each of the forms
class FeatureInlineAdmin(admin.StackedInline):
    extra = 0  # Allows us to show the 'Add another' link
    min_num = 3
    # We override the default template for stacked inlines so that we can
    # customize the label for each field
    template = 'admin/homepage/homepage/edit_inline/stacked.html'

    # To disable the icons that allow you to add/change the related models,
    # we set the flags that allow these operations to False on the widgets
    # associated with those related model fields. We override the formset
    # method to get access to those fields.
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        base_fields = formset.form.base_fields

        for field in base_fields:
            base_fields[field].widget.can_add_related = False
            base_fields[field].widget.can_change_related = False
            base_fields[field].label = 'Feature'

        return formset

    # Only superusers can add new homepage fields
    def has_add_permission(self, request):
        return request.user.is_superuser


class LeaderInlineAdmin(FeatureInlineAdmin):
    model = HomepageLeaders
    fields = ('leader',)


class NewsInlineAdmin(FeatureInlineAdmin):
    model = HomepageNews
    fields = ('news',)
    min_num = 4


class HighlightInlineAdmin(FeatureInlineAdmin):
    model = HomepageHighlights
    fields = ('highlights',)


class HomepageAdmin(SingletonAdmin):
    inlines = [
        LeaderInlineAdmin,
        NewsInlineAdmin,
        HighlightInlineAdmin,
    ]

    # We override this function so that we can rename the header shown for this
    # admin view
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Homepage Features'

        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )


admin.site.register(Homepage, HomepageAdmin)
