from django import shortcuts
from wagtail import models as wagtail_models

from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


class ProductIndexPage(foundation_metadata.FoundationMetadataPageMixin, wagtail_models.Page):
    """
    Index page to be the parent of all product pages.

    After the editorial content index was added to the buyer's guide, it was hard to find it, because it was mixed in
    with the long list of product pages. This product index page is added to group the product pages in a "folder" to
    make it easier to navigate in the admin.

    This page can not be visited directly, it redirects to its parent, the buyer's guide homepage.
    """

    parent_page_types = ["wagtailpages.BuyersGuidePage"]
    subpage_types = ["wagtailpages.GeneralProductPage"]

    def serve(self, request, *args, **kwargs):
        parent = self.get_parent()
        return shortcuts.redirect(to=parent.get_url())

    def serve_preview(self, request, mode_name):
        return self.serve(request=request)

