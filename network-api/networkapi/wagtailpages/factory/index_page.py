from wagtail_factories import PageFactory

from networkapi.wagtailpages.models import IndexPage


class IndexPageFactory(PageFactory):
    class Meta:
        model = IndexPage
