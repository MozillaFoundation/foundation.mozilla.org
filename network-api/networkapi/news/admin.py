from django.contrib import admin

from networkapi.news.models import News
from networkapi.news.forms import NewsAdminForm


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm


admin.site.register(News, NewsAdmin)
