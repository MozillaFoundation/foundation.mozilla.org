from wagtail_factories import PageFactory

from foundation_cms.legacy_cms.wagtailpages.models import IndexPage


class IndexPageFactory(PageFactory):
    class Meta:
        model = IndexPage
