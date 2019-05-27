from networkapi.wagtailpages.models import PrimaryPage
from .abstract import CMSPageFactory


class PrimaryPageFactory(CMSPageFactory):
    class Meta:
        model = PrimaryPage
