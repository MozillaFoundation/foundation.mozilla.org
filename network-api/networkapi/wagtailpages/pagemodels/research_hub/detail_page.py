from wagtail.core import models as wagtail_models

from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


class ResearchDetailPage(foundation_metadata.FoundationMetadataPageMixin, wagtail_models.Page):
    parent_page_types = ['ResearchLibraryPage']
