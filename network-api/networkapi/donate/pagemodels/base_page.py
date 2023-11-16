from wagtail.models import Page

from networkapi.wagtailpages.models import FoundationMetadataPageMixin
from networkapi.wagtailpages.pagemodels.mixin.foundation_navigation import (
    FoundationNavigationPageMixin,
)


class BaseDonationPage(FoundationMetadataPageMixin, FoundationNavigationPageMixin, Page):
    class Meta:
        abstract = True
