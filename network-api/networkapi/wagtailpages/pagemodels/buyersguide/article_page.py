from django import http
from wagtail.core import models as wagtail_models

from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


class BuyersGuideArticlePage(
    foundation_metadata.FoundationMetadataPageMixin,
    wagtail_models.Page
):
    parent_page_types = ['wagtailpages.BuyersGuideEditorialContentIndexPage']
    subpage_types = []
    template = 'pages/buyersguide/article_page.html'

    def get_context(self, request: http.HttpRequest, *args, **kwargs) -> dict:
        context = super().get_context(request, *args, **kwargs)
        context['home_page'] = self.get_parent().get_parent().specific
        return context

