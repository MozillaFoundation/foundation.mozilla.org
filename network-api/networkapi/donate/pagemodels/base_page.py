from wagtail.models import Page

from networkapi.wagtailpages.models import FoundationMetadataPageMixin


class BaseDonationPage(FoundationMetadataPageMixin, Page):
    class Meta:
        abstract = True
