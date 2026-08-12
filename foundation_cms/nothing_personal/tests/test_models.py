from wagtail.models import Page
from wagtail.test.utils import WagtailPageTestCase

from foundation_cms.core.models import HomePage
from foundation_cms.nothing_personal.models import (
    NothingPersonalArticleCollectionPage,
    NothingPersonalArticlePage,
    NothingPersonalHomePage,
    NothingPersonalPodcastPage,
    NothingPersonalProductCollectionPage,
    NothingPersonalProductReviewPage,
)
from foundation_cms.nothing_personal.models.home_page import NothingPersonalFeaturedItem
from foundation_cms.nothing_personal.models.product_review_page import ProductMentioned


class NothingPersonalModelTests(WagtailPageTestCase):
    def setUp(self):
        root_page = Page.get_first_root_node()
        self.core_home_page = self._add_page(root_page, HomePage, "Model Smoke Home", "model-smoke-home")
        self.nothing_personal_home_page = self._add_page(
            self.core_home_page,
            NothingPersonalHomePage,
            "Nothing Personal",
            "nothing-personal",
        )

    def test_nothing_personal_home_page_can_be_saved(self):
        self.nothing_personal_home_page.refresh_from_db()

        self.assertEqual(str(self.nothing_personal_home_page), "Nothing Personal")
        self.assertEqual(self.nothing_personal_home_page.get_parent().specific, self.core_home_page)

    def test_article_collection_page_can_be_saved(self):
        page = self._add_page(
            self.nothing_personal_home_page,
            NothingPersonalArticleCollectionPage,
            "Articles",
            "articles",
        )

        page.refresh_from_db()

        self.assertEqual(str(page), "Articles")
        self.assertEqual(page.get_parent().specific, self.nothing_personal_home_page)

    def test_article_page_can_be_saved(self):
        page = self._add_page(
            self.nothing_personal_home_page,
            NothingPersonalArticlePage,
            "Privacy Article",
            "privacy-article",
        )

        page.refresh_from_db()

        self.assertEqual(str(page), "Privacy Article")
        self.assertEqual(page.get_parent().specific, self.nothing_personal_home_page)

    def test_podcast_page_can_be_saved(self):
        page = self._add_page(
            self.nothing_personal_home_page,
            NothingPersonalPodcastPage,
            "Nothing Personal Podcast",
            "podcast",
        )

        page.refresh_from_db()

        self.assertEqual(str(page), "Nothing Personal Podcast")
        self.assertEqual(page.get_parent().specific, self.nothing_personal_home_page)

    def test_product_collection_page_can_be_saved(self):
        page = self._add_page(
            self.nothing_personal_home_page,
            NothingPersonalProductCollectionPage,
            "Product Reviews",
            "product-reviews",
        )

        page.refresh_from_db()

        self.assertEqual(str(page), "Product Reviews")
        self.assertEqual(page.get_parent().specific, self.nothing_personal_home_page)

    def test_product_review_page_can_be_saved(self):
        page = self._add_product_review("Private Messenger Review", "private-messenger-review")

        page.refresh_from_db()

        self.assertEqual(str(page), "Private Messenger Review")
        self.assertEqual(page.get_parent().specific, self.nothing_personal_home_page)

    def test_featured_item_can_be_saved(self):
        article = self._add_page(
            self.nothing_personal_home_page,
            NothingPersonalArticlePage,
            "Featured Article",
            "featured-article",
        )
        featured_item = NothingPersonalFeaturedItem.objects.create(
            home_page=self.nothing_personal_home_page,
            page=article,
        )

        featured_item.refresh_from_db()

        self.assertEqual(featured_item.home_page, self.nothing_personal_home_page)
        self.assertEqual(featured_item.page_id, article.pk)

    def test_product_mentioned_can_be_saved(self):
        owner = self._add_product_review("Owner Product", "owner-product")
        mentioned_product = self._add_product_review("Mentioned Product", "mentioned-product")
        product_mentioned = ProductMentioned.objects.create(
            page=owner,
            mentioned_product=mentioned_product,
        )

        product_mentioned.refresh_from_db()

        self.assertEqual(product_mentioned.page, owner)
        self.assertEqual(product_mentioned.mentioned_product, mentioned_product)
        self.assertEqual(str(product_mentioned), "Mentioned Product")

    def _add_product_review(self, title, slug):
        return self._add_page(
            self.nothing_personal_home_page,
            NothingPersonalProductReviewPage,
            title,
            slug,
        )

    def _add_page(self, parent, model, title, slug):
        page = model(
            title=title,
            slug=slug,
            seo_title=title,
            search_description=f"{title} description.",
        )
        parent.add_child(instance=page)
        return page
