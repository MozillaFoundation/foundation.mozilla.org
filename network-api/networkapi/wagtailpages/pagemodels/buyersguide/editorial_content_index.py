from wagtail.core import models as wagtail_models

from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


class BuyersGuideEditorialContentIndexPage(
    foundation_metadata.FoundationMetadataPageMixin,
    wagtail_models.Page,
):
    parent_page_types = ['wagtailpages.BuyersGuidePage']
    subpage_types = ['wagtailpages.BuyersGuideArticlePage']
    template = 'pages/buyersguide/editorial_content_index_page.html'

    def get_context(self, request, *args, **kwargs):
        context =  super().get_context(request, *args, **kwargs)
        context["home_page"] = self.get_parent().specific
        context["items"] = self.get_descendants().public().live()
        return context
