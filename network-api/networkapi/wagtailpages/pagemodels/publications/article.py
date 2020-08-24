from wagtail.core.models import Page

from ..mixin.foundation_metadata import FoundationMetadataPageMixin


class ArticlePage(FoundationMetadataPageMixin, Page):

    """

    Article belong to PublicationPages
    An Article can only belong to one Chapter/Publication Page
    An ArticlePage can have no children

    ? If these only belong to PublicationPages, should be extra explicit and call it PublicationArticlePage?
    """
    pass
