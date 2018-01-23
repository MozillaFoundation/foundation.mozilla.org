from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from networkapi.landingpage.models import (
    LandingPage,
    Signup,
)


class LandingPageAdmin(PageAdmin):
    fieldsets = (
        (None, {
            'fields': [
                'title',
                'header',
                'content',
                'signup',
            ]
        }),
        ('Publishing', {
            'fields': [
                'status',
                ('publish_date', 'expiry_date'),

            ]
        }),
        ('Ask Survey', {
            'fields': [
                'survey_id'
            ],
            'classes': ('collapse-closed',)
        }),
        ('Meta data', {
            'fields': ['_meta_title', 'slug',
                       ('description', 'gen_description')],
            'classes': ('collapse-closed',)
        }),
    )

admin.site.register(LandingPage, LandingPageAdmin)
admin.site.register(Signup)
