from wagtail.core import models as wagtail_models

from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


class ResearchHubBasePage(
    foundation_metadata.FoundationMetadataPageMixin,
    wagtail_models.Page,
):
    class Meta:
        abstract = True
