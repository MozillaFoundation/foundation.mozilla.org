# Solution came from Aleksi44 on Github:
# https://github.com/wagtail/wagtail/issues/6583#issuecomment-798960446
from django.contrib.sitemaps import views as sitemap_views
from wagtail.contrib.sitemaps.sitemap_generator import Sitemap


class CustomSitemap(Sitemap):

    def items(self):
        return (
            self.get_wagtail_site()
                .root_page
                .localized  # This is missing from sitemap_generator
                .get_descendants(inclusive=True)
                .live()
                .public()
                .order_by('path')
                .specific())


def sitemap(request, **kwargs):
    sitemaps = {'wagtail': CustomSitemap(request)}
    return sitemap_views.sitemap(request, sitemaps, **kwargs)
