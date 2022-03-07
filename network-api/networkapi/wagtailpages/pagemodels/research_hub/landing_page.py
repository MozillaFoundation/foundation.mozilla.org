from wagtail.core import models as wagtail_models

from networkapi.wagtailpages.pagemodels.mixin import foundation_metadata


class ResearchLandingPage(foundation_metadata.FoundationMetadataPageMixin, wagtail_models.Page):
    max_count = 1
    subpage_types = [
        'ResearchLibraryPage',
        'ResearchAuthorsIndexPage',
    ]
