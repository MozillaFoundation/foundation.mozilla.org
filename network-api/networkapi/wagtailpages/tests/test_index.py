from http import HTTPStatus

from django import test
from wagtail.core import models as wagtail_models


from networkapi.wagtailpages.factory import bannered_campaign_page as bannered_factory
from networkapi.wagtailpages.factory import index_page as index_factory
from networkapi.wagtailpages.factory import publication as publication_factory
from networkapi.wagtailpages.tests import base as test_base


# TODO: We should be able to remove this when the cache is not needed anymore.
@test.override_settings(CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}})
class IndexPageTests(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.index_page = index_factory.IndexPageFactory(parent=cls.homepage)

    def test_serve_children_in_entries(self):
        """
        Currently, this is returning the generic page type, which requires the use of
        `.specific` in the templates. That is probably causing the n+1 which the cache is
        used to cricumvent. We should probably not be doing that in the template and return
        the proper pages in the context.

        TODO: Refactor implementation to return specific page types of child pages.
        """
        article_page_1 = publication_factory.ArticlePageFactory(parent=self.index_page)
        generic_of_article_page_1 = wagtail_models.Page.objects.get(id=article_page_1.id)
        article_page_2 = publication_factory.ArticlePageFactory(parent=self.index_page)
        generic_of_article_page_2 = wagtail_models.Page.objects.get(id=article_page_2.id)

        response = self.client.get(path=self.index_page.get_url())

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(generic_of_article_page_1, response.context["entries"])
        self.assertIn(generic_of_article_page_2, response.context["entries"])

    def test_serve_children_of_different_types_in_entries(self):
        """
        Currently, this is returning the generic page type, which requires the use of
        `.specific` in the templates. That is probably causing the n+1 which the cache is
        used to cricumvent. We should probably not be doing that in the template and return
        the proper pages in the context.

        TODO: Refactor implementation to return specific page types of child pages.
        """
        article_page = publication_factory.ArticlePageFactory(parent=self.index_page)
        generic_of_article_page = wagtail_models.Page.objects.get(id=article_page.id)
        bannered_page = bannered_factory.BanneredCampaignPageFactory(parent=self.index_page)
        generic_of_bannered_page = wagtail_models.Page.objects.get(id=bannered_page.id)

        response = self.client.get(path=self.index_page.get_url())

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(generic_of_article_page, response.context["entries"])
        self.assertIn(generic_of_bannered_page, response.context["entries"])

    def test_serve_entries_have_same_locale_as_index_page(self):
        article_page = publication_factory.ArticlePageFactory(parent=self.index_page)
        self.synchronize_tree()
        fr_index_page = self.index_page.get_translation(self.fr_locale)

        response = self.client.get(path=fr_index_page.get_url())

        self.assertEqual(response.status_code, HTTPStatus.OK)
        fr_entry_page = response.context["entries"][0]
        self.assertNotEqual(fr_entry_page.id, article_page.id)
        self.assertEqual(fr_entry_page.locale, self.fr_locale)

    def test_entries_by_tag_route(self):
        """
        Show only the entries with the filtered tag.

        Interestingly, the current filter implementation is resolving the pages to their specific type when filtering
        by tag.

        """
        # Tagged page
        TEST_TAG = "test-tag"
        tagged_page = bannered_factory.BanneredCampaignPageFactory(parent=self.index_page)
        tagged_page.tags.add(TEST_TAG)
        tagged_page.save()
        # Untagged page
        untagged_page = bannered_factory.BanneredCampaignPageFactory(parent=self.index_page)
        # Differently tagged page
        differently_tagged_page = bannered_factory.BanneredCampaignPageFactory(parent=self.index_page)
        differently_tagged_page.tags.add("differnt-tag")
        differently_tagged_page.save()
        #
        path = (
            self.index_page.get_url()
            +  self.index_page.reverse_subpage('entries_by_tag', kwargs={"tag": TEST_TAG})
        )

        response = self.client.get(path=path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(tagged_page, response.context["entries"])
        self.assertNotIn(untagged_page, response.context["entries"])
        self.assertNotIn(differently_tagged_page, response.context["entries"])
