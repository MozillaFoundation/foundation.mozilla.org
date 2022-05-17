from wagtail.core import models as wagtail_models

from networkapi.wagtailpages import utils
from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


class ResearchHubBasePage(
    foundation_metadata.FoundationMetadataPageMixin,
    wagtail_models.Page,
):

    def get_context(self, request):
        context = super().get_context(request)
        context = utils.set_main_site_nav_information(self, context, "Homepage")
        return context

    class Meta:
        abstract = True
