
from wagtail.core.models import Page

from ..mixin.foundation_metadata import FoundationMetadataPageMixin


class PublicationPage(FoundationMetadataPageMixin, Page):
    """
    This is the root page of a publication. From here the user can browse to the various sections (called chapters).
    It will have information on the publication, its authors, and metadata from it's children
    """

    # TODO: once we make chapter pages, add that as a subpage type
    subpage_types = []
