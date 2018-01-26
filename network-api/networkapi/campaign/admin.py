from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from networkapi.campaign.models import (
    Campaign,
    Petition,
)


class CampaignAdmin(PageAdmin):
    fieldsets = (
        (None, {
            'fields': [
                'title',
                'header',
                'content',
                'petition',
            ]
        }),
        ('Publishing', {
            'fields': [
                'status',
                ("publish_date", "expiry_date"),

            ]
        }),
        ("Meta data", {
            "fields": ["_meta_title", "slug",
                       ("description", "gen_description")],
            "classes": ("collapse-closed",)
        }),
    )


admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Petition)
