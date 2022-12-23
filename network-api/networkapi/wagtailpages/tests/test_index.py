from http import HTTPStatus

from wagtail.core import models as wagtail_models

from networkapi.wagtailpages.factory import index_page as index_factory
from networkapi.wagtailpages.factory import publication as publication_factory
from networkapi.wagtailpages.tests import base as test_base


class IndexPageTests(test_base.WagtailpagesTestCase):
    def test_GET_child_in_entries(self):
        """
        Currently, this is returning the generic page type, which requires the use of
        `.specific` in the templates. That is probably causing the n+1 which the cache is
        used to cricumvent. We should probably not be doing that in the template and return
        the proper pages in the context.

        TODO: Refactor implementation to return specific page types of child pages.
        """
        index_page = index_factory.IndexPageFactory(parent=self.homepage)
        article_page = publication_factory.ArticlePageFactory(parent=index_page)
        generic_child_page = wagtail_models.Page.objects.get(id=article_page.id)

        response = self.client.get(path=index_page.get_url())

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(generic_child_page, response.context["entries"])


