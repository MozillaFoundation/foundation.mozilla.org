from wagtail.core import models as wagtail_models

from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


class BuyersGuideEditorialContentIndexPage(
    foundation_metadata.FoundationMetadataPageMixin,
    wagtail_models.Page,
):
    parent_page_types = ['wagtailpages.BuyersGuidePage']
    subpage_types = ['wagtailpages.BuyersGuideArticlePage']
    template = 'pages/buyersguide_editorial_content_index_page.html'
