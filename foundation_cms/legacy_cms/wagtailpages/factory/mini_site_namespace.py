from wagtail_factories import PageFactory

from foundation_cms.legacy_cms.wagtailpages.models import MiniSiteNameSpace


class MiniSiteNamespaceFactory(PageFactory):
    class Meta:
        model = MiniSiteNameSpace
