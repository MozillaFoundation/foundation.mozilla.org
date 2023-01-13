import datetime
from http import HTTPStatus

from django import test
from wagtail.core import models as wagtail_models
import wagtail_factories

from networkapi.wagtailpages.factory import bannered_campaign_page as bannered_factory
from networkapi.wagtailpages.factory import index_page as index_factory
from networkapi.wagtailpages.factory import publication as publication_factory
from networkapi.wagtailpages.tests import base as test_base
from networkapi.wagtailpages.pagemodels import index


# TODO: We should be able to remove this when the cache is not needed anymore.
@test.override_settings(CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}})
class IndexPageTestCase(test_base.WagtailpagesTestCase):
    index_page_factory: wagtail_factories.PageFactory = index_factory.IndexPageFactory
    page_size = index.IndexPage.PAGE_SIZES[0][0]

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.index_page = cls.index_page_factory(
            parent=cls.homepage,
            page_size=cls.page_size,
        )

    def generate_enough_child_pages_to_fill_number_of_index_pages(
        self,
        index_pages_to_fill: int = 1,
        base_title: str = "Test child title",
        child_page_factory: wagtail_factories.PageFactory = publication_factory.ArticlePageFactory,
    ):
        """
        Make enough child pages to fill given number of index pages.

        Child pages are ordered newest to oldest.

        All pages also use the same `base_title` for their `title`. For each page,
        a number is appended to the `base_title` in order of their creation. That
        means the oldest page has a `title = base_title + " 1"`.

        """
        tz = datetime.timezone.utc
        child_page_count = self.index_page.page_size * index_pages_to_fill
        child_pages = []
        for index in range(0, child_page_count):
            child_pages.append(
                child_page_factory(
                    parent=self.index_page,
                    title=base_title + f" {index + 1}",
                    first_published_at=(
                        datetime.datetime(2020, 1, 1, tzinfo=tz)
                        + datetime.timedelta(days=index)
                    ),
                )
            )
        child_pages.reverse()
        return child_pages


class IndexPageTests(IndexPageTestCase):
    def test_factory(self):
        self.index_page_factory()

        self.assertTrue(True)

    def test_page_loads_emtpy(self):
        response = self.client.get(self.index_page.get_url())

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_page_loads(self):
        self.generate_enough_child_pages_to_fill_number_of_index_pages(1)

        response = self.client.get(self.index_page.get_url())

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "wagtailpages/fragments/entry_cards_item_loop.html")
        self.assertTemplateUsed(response, "wagtailpages/index_page.html")

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

    def test_generate_entries_set_html_route_page_2_of_3(self):
        """
        Get JSON containing HTML fragment of second page of entries.

        The second page is returned by default from the entries endpoint, no page parameter is necessary.

        Availability of a follow up page needs to be indicated.

        Currently, this is returning the generic page type, which requires the use of
        `.specific` in the templates. That is probably causing the n+1 which the cache is
        used to cricumvent. We should probably not be doing that in the template and return
        the proper pages in the context.

        TODO: Refactor implementation to return specific page types of child pages.
        """
        page_size = self.index_page.page_size
        children = self.generate_enough_child_pages_to_fill_number_of_index_pages(3)
        first_page_children_ids = [c.id for c in children[:page_size]]
        second_page_children_ids = [c.id for c in children[page_size:2*page_size]]
        third_page_children_ids = [c.id for c in children[2*page_size:]]
        first_page_children = wagtail_models.Page.objects.filter(id__in=first_page_children_ids)
        second_page_children = wagtail_models.Page.objects.filter(id__in=second_page_children_ids)
        third_page_children = wagtail_models.Page.objects.filter(id__in=third_page_children_ids)
        path = self.index_page.get_url() + self.index_page.reverse_subpage("generate_entries_set_html")

        response = self.client.get(path=path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "wagtailpages/fragments/entry_cards_item_loop.html")
        self.assertTemplateNotUsed(response, "wagtailpages/index_page.html")
        entries = response.context["entries"]
        for child in first_page_children:
            self.assertNotIn(child, entries)
        for child in second_page_children:
            self.assertIn(child, entries)
        for child in third_page_children:
            self.assertNotIn(child, entries)
        self.assertTrue(response.json()["has_next"])

    def test_generate_entries_set_html_route_page_3_of_3(self):
        """
        Get JSON containing HTML fragment of third page of entries.

        The third page needs to be requested with a queryparameter.

        It should be indicated that no following page is available.

        Currently, this is returning the generic page type, which requires the use of
        `.specific` in the templates. That is probably causing the n+1 which the cache is
        used to cricumvent. We should probably not be doing that in the template and return
        the proper pages in the context.

        TODO: Refactor implementation to return specific page types of child pages.
        """
        page_size = self.index_page.page_size
        children = self.generate_enough_child_pages_to_fill_number_of_index_pages(3)
        first_page_children_ids = [c.id for c in children[:page_size]]
        second_page_children_ids = [c.id for c in children[page_size:2*page_size]]
        third_page_children_ids = [c.id for c in children[2*page_size:]]
        first_page_children = wagtail_models.Page.objects.filter(id__in=first_page_children_ids)
        second_page_children = wagtail_models.Page.objects.filter(id__in=second_page_children_ids)
        third_page_children = wagtail_models.Page.objects.filter(id__in=third_page_children_ids)
        path = (
            self.index_page.get_url()
            + self.index_page.reverse_subpage("generate_entries_set_html")
            + "?page=2"  # Pages are 0-based, so the third page has number 2.
        )

        response = self.client.get(path=path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        entries = response.context["entries"]
        for child in first_page_children:
            self.assertNotIn(child, entries)
        for child in second_page_children:
            self.assertNotIn(child, entries)
        for child in third_page_children:
            self.assertIn(child, entries)
        self.assertFalse(response.json()["has_next"])

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
        differently_tagged_page.tags.add("different-tag")
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

    # TODO: Test pagination and tag filtering
