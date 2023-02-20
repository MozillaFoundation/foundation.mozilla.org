from wagtail import models as wagtail_models

from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


class ProductIndexPage(foundation_metadata.FoundationMetadataPageMixin, wagtail_models.Page):
    parent_page_types = ["wagtailpages.BuyersGuidePage"]
    subpage_types = ["wagtailpages.GeneralProductPage"]
