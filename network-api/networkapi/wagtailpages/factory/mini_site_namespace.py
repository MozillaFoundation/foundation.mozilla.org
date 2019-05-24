from networkapi.wagtailpages.models import MiniSiteNameSpace
from wagtail_factories import PageFactory


class MiniSiteNamespaceFactory(PageFactory):
    class Meta:
        model = MiniSiteNameSpace
