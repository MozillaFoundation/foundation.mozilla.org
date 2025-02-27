from wagtail_factories import PageFactory

from legacy_cms.wagtailpages.models import MiniSiteNameSpace


class MiniSiteNamespaceFactory(PageFactory):
    class Meta:
        model = MiniSiteNameSpace
