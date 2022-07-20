from wagtail.core import models as wagtail_models


class BuyersGuideArticleIndexPage(wagtail_models.Page):
    parent_page_types = ['wagtailpages.BuyersGuidePage']
