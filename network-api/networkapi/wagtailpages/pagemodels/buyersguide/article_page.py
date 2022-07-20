from wagtail.core import models as wagtail_models


class BuyersGuideArticlePage(wagtail_models.Page):
    parent_page_types = ['wagtailpages.BuyersGuideEditorialContentIndexPage']
