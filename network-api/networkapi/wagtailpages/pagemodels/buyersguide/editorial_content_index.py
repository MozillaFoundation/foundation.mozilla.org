from wagtail.core import models as wagtail_models


class BuyersGuideEditorialContentIndexPage(wagtail_models.Page):
    parent_page_types = ['wagtailpages.BuyersGuidePage']
    subpage_types = ['wagtailpages.BuyersGuideArticlePage']
    template = 'pages/buyers_guide_editorial_content_index_page.html'
