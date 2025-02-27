from wagtail_factories import PageFactory

from legacy_cms.wagtailpages.models import IndexPage


class IndexPageFactory(PageFactory):
    class Meta:
        model = IndexPage
