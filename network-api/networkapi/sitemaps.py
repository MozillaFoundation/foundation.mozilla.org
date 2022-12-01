# Solution came from Aleksi44 on Github:
# https://github.com/wagtail/wagtail/issues/6583#issuecomment-798960446
from django.conf import settings
from django.contrib.sitemaps import views as sitemap_views
from django.shortcuts import render
from wagtail.contrib.sitemaps.sitemap_generator import Sitemap


class CustomSitemap(Sitemap):
    def items(self):
        return (
            self.get_wagtail_site()
            .root_page.localized.get_descendants(inclusive=True)  # This is missing from sitemap_generator
            .live()
            .public()
            .order_by("path")
            .specific()
        )


def sitemap(request, **kwargs):
    sitemaps = {"wagtail": CustomSitemap(request)}
    return sitemap_views.sitemap(request, sitemaps, **kwargs)


def sitemap_index(request):
    context = {}
    context["languages"] = [lang[0] for lang in settings.LANGUAGES]
    context["domain"] = "https://foundation.mozilla.org"

    return render(request, "sitemap-index.xml", context, content_type="text/xml")
