from wagtail_factories import PageFactory

from networkapi.wagtailpages.models import MiniSiteNameSpace


class MiniSiteNamespaceFactory(PageFactory):
    class Meta:
        model = MiniSiteNameSpace
