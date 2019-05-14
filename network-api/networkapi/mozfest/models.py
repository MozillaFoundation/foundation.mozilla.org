from networkapi.wagtailpages.models import FoundationMetadataPageMixin
from wagtail.core.models import Page


class MozfestPrimaryPage(FoundationMetadataPageMixin, Page):
    pass


class MozfestHomepage(MozfestPrimaryPage):
    subpage_types = [
        'MozfestPrimaryPage'
    ]
