from networkapi.wagtailpages.factory import publication as publication_factory
from networkapi.wagtailpages.tests import base as test_base


class PublicationPageTest(test_base.WagtailpagesTestCase):
    def test_factory(self):
        publication_factory.PublicationPageFactory()
