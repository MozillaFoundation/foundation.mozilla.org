from networkapi.wagtailpages.models import IndexPage
from wagtail_factories import PageFactory


class IndexPageFactory(PageFactory):
    class Meta:
        model = IndexPage
