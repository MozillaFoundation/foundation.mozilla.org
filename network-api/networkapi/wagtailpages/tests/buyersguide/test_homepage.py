from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from django.test.utils import override_settings
from wagtail.models import Locale, Page, Site

from networkapi.utility.faker.helpers import reseed
from networkapi.wagtailpages.factory import buyersguide as buyersguide_factories
from networkapi.wagtailpages.factory.homepage import WagtailHomepageFactory
from networkapi.wagtailpages.pagemodels.base import Homepage
from networkapi.wagtailpages.pagemodels.buyersguide.article_page import (
    BuyersGuideArticlePage,
)
from networkapi.wagtailpages.pagemodels.buyersguide.campaign_page import (
    BuyersGuideCampaignPage,
)
from networkapi.wagtailpages.pagemodels.buyersguide.homepage import BuyersGuidePage
from networkapi.wagtailpages.pagemodels.buyersguide.products import (
    BuyersGuideProductCategory,
    ProductPage,
    ProductPageCategory,
)
from networkapi.wagtailpages.tests.buyersguide.base import BuyersGuideTestCase


class TestFactories(TestCase):
    def test_homepage_factory(self):
        buyersguide_factories.BuyersGuidePageFactory()

    def test_hero_supporting_page_relation_factory(self):
        buyersguide_factories.BuyersGuidePageHeroSupportingPageRelationFactory()

    def test_featured_article_relation_factory(self):
        buyersguide_factories.BuyersGuidePageFeaturedArticleRelationFactory()

    def test_featured_update_relation_factory(self):
        buyersguide_factories.BuyersGuidePageFeaturedUpdateRelationFactory()


@override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
class BuyersGuideViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testuser password",
        )
        buyersguide = BuyersGuidePage.objects.first()
        if not buyersguide:
            homepage = Homepage.objects.first()
            if not homepage:
                site_root = Page.objects.first()
                homepage = WagtailHomepageFactory.create(
                    parent=site_root,
                    title="Homepage",
                    slug="homepage",
                    hero_image__file__width=1080,
                    hero_image__file__height=720,
                )
            site = Site.objects.first()
            site.root_page = homepage
            site.save()
            # Create the buyersguide page.
            buyersguide = BuyersGuidePage()
            buyersguide.title = "Privacy not included"
            buyersguide.slug = "privacynotincluded"
            homepage.add_child(instance=buyersguide)
            buyersguide.save_revision().publish()
            locale = Locale.objects.create(language_code="fr")
            buyersguide.copy_for_translation(locale, copy_parents=True, alias=True)

    def test_homepage(self):
        """
        Test that the homepage works.
        """
        response = self.client.get("/privacynotincluded/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/en/privacynotincluded/",
            "Homepage should be forwarded to /en/ by default",
        )

    def test_localised_homepage(self):
        """
        Test that the homepage redirects properly under different locale configurations.
        """
        response = self.client.get("/privacynotincluded", follow=True, headers={"accept-language": "fr"})
        self.assertEqual(
            response.redirect_chain[0][0],
            "/fr/privacynotincluded/",
            "redirects according to HTTP_ACCEPT_LANGUAGE",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/privacynotincluded", follow=True, headers={"accept-language": "sw"})
        self.assertEqual(
            response.redirect_chain[0][0],
            "/sw/privacynotincluded/",
            "redirects according to HTTP_ACCEPT_LANGUAGE for non-existent locale",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/privacynotincluded", follow=True, headers={"accept-language": "foo"})
        self.assertEqual(
            response.redirect_chain[0][0],
            "/en/privacynotincluded/",
            "redirects to /en/ by default",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/de/privacynotincluded", follow=True, headers={"accept-language": "it"})
        self.assertEqual(
            response.redirect_chain[0][0],
            "/de/privacynotincluded/",
            "no redirect from hardcoded locale",
        )
        self.assertEqual(response.status_code, 200)

    def test_product_view_404(self):
        """
        Test that the product view raises an Http404 if the product name doesn't exist
        """
        response = self.client.get("/en/privacynotincluded/products/this is not a product", follow=True)
        self.assertEqual(response.status_code, 404, "this is not a product")

        response = self.client.get("/en/privacynotincluded/products/this is not a product/")
        self.assertEqual(response.status_code, 404, "this is not a product")

    def test_category_view_404(self):
        """
        Test that the category view raises an Http404 if the category name doesn't exist
        """
        response = self.client.get("/en/privacynotincluded/categories/this is not a category", follow=True)
        self.assertEqual(response.status_code, 404, "this is not a category")

        response = self.client.get("/en/privacynotincluded/categories/this is not a category/")
        self.assertEqual(response.status_code, 404, "this is not a category")

    def test_category_view(self):
        """
        Test that the category view returns a 302 for /privacynotincluded/ to /en/privacynotincluded/
        for both slug-based and name-based categories.
        """
        response = self.client.get("/privacynotincluded/categories/Smart%20Home/")
        self.assertEqual(response.status_code, 302, 'The category "Smart Home" should work by name')

        response = self.client.get("/privacynotincluded/categories/smart-home/")
        self.assertEqual(response.status_code, 302, 'The category "Smart Home" should work by slug')


# Use dummy caching for BuyersGuide URLs.
@override_settings(CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}})
@override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
class TestBuyersGuidePage(BuyersGuideTestCase):
    request_factory = RequestFactory()

    def test_buyersguide_url(self):
        self.assertEqual(self.bg.slug, "privacynotincluded")
        response = self.client.get(self.bg.url)
        self.assertEqual(response.status_code, 200)

    def test_serve_page(self):
        response = self.client.get(self.bg.url)

        self.assertEqual(response.status_code, 200)

    def test_serve_page_no_products(self):
        products = ProductPage.objects.descendant_of(self.bg)
        products.delete()
        self.assertEqual(products.count(), 0)
        query_number = 47

        with self.assertNumQueries(query_number):
            response = self.client.get(self.bg.url)

            self.assertEqual(response.status_code, 200)

    def test_serve_page_one_product(self):
        products = ProductPage.objects.descendant_of(self.bg)
        self.assertEqual(products.count(), 1)
        query_number = 62

        with self.assertNumQueries(query_number):
            response = self.client.get(self.bg.url)

            self.assertEqual(response.status_code, 200)

    def test_serve_page_many_products(self):
        reseed(12345)
        additional_products_count = 49
        for _ in range(additional_products_count):
            buyersguide_factories.ProductPageFactory(parent=self.bg, with_random_categories=True)
        products = ProductPage.objects.descendant_of(self.bg)
        self.assertEqual(products.count(), additional_products_count + 1)
        query_number = 63

        with self.assertNumQueries(query_number):
            response = self.client.get(self.bg.url)

            self.assertEqual(response.status_code, 200)

    def test_serve_page_many_products_logged_in(self):
        reseed(12345)
        additional_products_count = 49
        for _ in range(additional_products_count):
            buyersguide_factories.ProductPageFactory(parent=self.bg, with_random_categories=True)
        products = ProductPage.objects.descendant_of(self.bg)
        self.assertEqual(products.count(), additional_products_count + 1)
        query_number = 69
        self.client.force_login(user=self.create_test_user())

        with self.assertNumQueries(query_number):
            response = self.client.get(self.bg.url)

            self.assertEqual(response.status_code, 200)

    def test_get_context_no_products(self):
        products = ProductPage.objects.descendant_of(self.bg)
        products.delete()
        self.assertEqual(products.count(), 0)
        request = self.request_factory.get(self.bg.url)
        request.user = AnonymousUser()
        request.LANGUAGE_CODE = "en"
        query_number = 6

        with self.assertNumQueries(query_number):
            self.bg.get_context(request=request)

    def test_get_context_one_product(self):
        products = ProductPage.objects.descendant_of(self.bg)
        self.assertEqual(products.count(), 1)
        request = self.request_factory.get(self.bg.url)
        request.user = AnonymousUser()
        request.LANGUAGE_CODE = "en"
        query_number = 9

        with self.assertNumQueries(query_number):
            self.bg.get_context(request=request)

    def test_get_context_one_product_one_category(self):
        products = ProductPage.objects.descendant_of(self.bg)
        product = products.first()
        BuyersGuideProductCategory.objects.all().delete()

        buyersguide_factories.ProductPageCategoryFactory(product=product)

        request = self.request_factory.get(self.bg.url)
        request.user = AnonymousUser()
        request.LANGUAGE_CODE = "en"
        query_number = 10

        with self.assertNumQueries(query_number):
            self.bg.get_context(request=request)

    def test_get_context_many_products(self):
        reseed(12345)
        additional_products_count = 49
        for _ in range(additional_products_count):
            buyersguide_factories.ProductPageFactory(parent=self.bg)
        products = ProductPage.objects.descendant_of(self.bg)
        self.assertEqual(products.count(), additional_products_count + 1)
        request = self.request_factory.get(self.bg.url)
        request.user = AnonymousUser()
        request.LANGUAGE_CODE = "en"
        query_number = 9

        with self.assertNumQueries(query_number):
            self.bg.get_context(request=request)

    def test_get_context_many_products_many_categories(self):
        reseed(12345)
        additional_products_count = 49
        for _ in range(additional_products_count):
            buyersguide_factories.ProductPageFactory(parent=self.bg, with_random_categories=True)
        products = ProductPage.objects.descendant_of(self.bg)
        self.assertEqual(products.count(), additional_products_count + 1)
        request = self.request_factory.get(self.bg.url)
        request.user = AnonymousUser()
        request.LANGUAGE_CODE = "en"
        query_number = 10

        with self.assertNumQueries(query_number):
            self.bg.get_context(request=request)

    def test_get_context_many_products_logged_in_user(self):
        reseed(12345)
        additional_products_count = 49
        for _ in range(additional_products_count):
            buyersguide_factories.ProductPageFactory(parent=self.bg)
        products = ProductPage.objects.descendant_of(self.bg)
        self.assertEqual(products.count(), additional_products_count + 1)
        user = self.create_test_user()
        self.client.force_login(user=user)
        request = self.request_factory.get(self.bg.url)
        request.user = user
        request.LANGUAGE_CODE = "en"
        query_number = 9

        with self.assertNumQueries(query_number):
            self.bg.get_context(request=request)

    def about_url_test(self, view_name, target_url, template):
        url = self.bg.reverse_subpage(view_name)
        self.assertEqual(url, target_url)
        response = self.client.get(self.bg.url + url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f"pages/buyersguide/about/{template}.html")

    def test_buyersguide_about_how_to_use_view(self):
        self.about_url_test("how-to-use-view", "about/", "how_to_use")

    def test_buyersguide_about_why_view(self):
        self.about_url_test("about-why-view", "about/why/", "why_we_made")

    def test_buyersguide_about_press_view(self):
        self.about_url_test("press-view", "about/press/", "press")

    def test_buyersguide_about_contact_view(self):
        self.about_url_test("contact-view", "about/contact/", "contact")

    def test_buyersguide_about_methodology_view(self):
        self.about_url_test("methodology-view", "about/methodology/", "methodology")

    def test_contest_page(self):
        url = self.bg.reverse_subpage("contest")
        self.assertEqual(url, "contest/")
        response = self.client.get(self.bg.url + url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/buyersguide/contest.html")

    def test_buyersguide_category_route(self):
        # Missing category
        missing_category = "missing-category-slug"
        category_url = self.bg.reverse_subpage("category-view", args=(missing_category,))
        self.assertEqual(category_url, f"categories/{missing_category}/")

        full_url = self.bg.url + category_url
        response = self.client.get(full_url)
        self.assertEqual(response.status_code, 404)

        category = BuyersGuideProductCategory.objects.first()
        response = self.client.get(f"/en/{self.bg.slug}/categories/{category.slug}/")
        self.assertEqual(response.status_code, 200)

    def test_buyersguide_product_redirect_route(self):
        response = self.client.get(self.bg.url)
        self.assertEqual(response.status_code, 200)

        product = self.get_or_create_product_page()
        response = self.client.get(product.url)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"/en/{self.bg.slug}/products/{product.slug}/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0], product.url)

    def test_sitemap_entries(self):
        categories = []
        for _ in range(3):
            cat = buyersguide_factories.BuyersGuideProductCategoryFactory(locale=self.default_locale)
            buyersguide_factories.BuyersGuideCategoryNavRelationFactory(category=cat)
            categories.append(cat)

        category_not_in_sitemap = buyersguide_factories.BuyersGuideProductCategoryFactory(locale=self.default_locale)

        response = self.client.get("/en/sitemap.xml")
        context = response.context

        self.assertEqual(context.template_name, "sitemap.xml")
        self.assertContains(response, "about/")
        self.assertContains(response, "about/why/")
        self.assertContains(response, "about/press/")
        self.assertContains(response, "about/contact/")
        self.assertContains(response, "about/methodology/")

        for category in categories:
            self.assertContains(response, f"categories/{category.slug}/")

        # Should not include categories that are not defined in the category nav
        self.assertNotContains(response, f"categories/{category_not_in_sitemap.slug}/")

    def test_empty_products_url(self):
        products_page = self.bg.url + "products/"
        response = self.client.get(products_page)
        self.assertEqual(response.status_code, 404)

    def test_empty_categories_url(self):
        categories_page = self.bg.url + "categories/"
        response = self.client.get(categories_page)
        self.assertEqual(response.status_code, 404)

    def test_category_filter_view(self):
        category = BuyersGuideProductCategory.objects.first()
        url = self.bg.url + self.bg.reverse_subpage("category-view", args=(category.slug,))

        # Need to set dummy cache
        with self.settings(CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context["products"]), 1)

            # Add BuyersGuideProductCategory
            category_orderable = ProductPageCategory(
                product=self.product_page,
                category=category,
            )
            category_orderable.save()
            self.product_page.product_categories.add(category_orderable)
            self.product_page.save_revision().publish()

            response = self.client.get(url)
            self.assertEqual(len(response.context["products"]), 1)

    def test_get_editorial_content_index(self):
        """Returns the editorial content index page."""
        editorial_content_index = buyersguide_factories.BuyersGuideEditorialContentIndexPageFactory(parent=self.bg)

        result = self.bg.get_editorial_content_index()

        self.assertEqual(result, editorial_content_index)

    def test_get_editorial_content_index_no_such_page(self):
        """Returns None when there is no editorial content index page."""
        result = self.bg.get_editorial_content_index()

        self.assertEqual(result, None)

    def test_bg_home_page_with_cta(self):
        cta = buyersguide_factories.BuyersGuideCallToActionFactory()
        self.bg.call_to_action = cta
        self.bg.save()

        response = self.client.get(self.bg.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(cta, response.context["featured_cta"])

    def test_bg_home_page_with_no_cta(self):
        self.bg.call_to_action = None
        self.bg.save()
        response = self.client.get(self.bg.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["featured_cta"])

    def test_category_page_context_with_cta_disabled(self):
        category = BuyersGuideProductCategory.objects.first()
        category.show_cta = False
        category.save()

        url = self.bg.url + self.bg.reverse_subpage("category-view", args=(category.slug,))

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["featured_cta"])

    def test_category_page_context_with_cta_enabled(self):
        cta = buyersguide_factories.BuyersGuideCallToActionFactory()
        self.bg.call_to_action = cta
        self.bg.save()
        category = BuyersGuideProductCategory.objects.first()
        category.show_cta = True
        category.save()

        url = self.bg.url + self.bg.reverse_subpage("category-view", args=(category.slug,))

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(cta, response.context["featured_cta"])


class TestBuyersGuidePageRelatedArticles(BuyersGuideTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.content_index = buyersguide_factories.BuyersGuideEditorialContentIndexPageFactory(
            parent=cls.bg,
        )

    def test_get_hero_featured_page_with_article_page(self):
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory.create(
            parent=self.content_index,
        )
        self.bg.hero_featured_page = article_page

        result = self.bg.get_hero_featured_page()

        self.assertEqual(result, article_page)
        self.assertEqual(type(result), BuyersGuideArticlePage)

    def test_get_hero_featured_page_with_campaign_page(self):
        campaign_page = buyersguide_factories.BuyersGuideCampaignPageFactory.create(
            parent=self.content_index,
        )
        self.bg.hero_featured_page = campaign_page

        result = self.bg.get_hero_featured_page()

        self.assertEqual(result, campaign_page)
        self.assertEqual(type(result), BuyersGuideCampaignPage)

    def test_get_hero_featured_page_not_set(self):
        self.bg.hero_featured_page = None

        result = self.bg.get_hero_featured_page()

        self.assertIsNone(result)

    def test_get_hero_featured_page_with_article_page_non_default_locale(self):
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
        )
        self.bg.hero_featured_page = article_page
        self.bg.save()
        self.synchronize_tree()
        buyersguide_homepage_fr = self.bg.get_translation(self.fr_locale)
        article_page_fr = article_page.get_translation(self.fr_locale)
        self.activate_locale(self.fr_locale)

        result = buyersguide_homepage_fr.get_hero_featured_page()

        self.assertEqual(result, article_page_fr)
        self.assertEqual(type(result), BuyersGuideArticlePage)

    def test_get_hero_featured_page_with_campaign_page_non_default_locale(self):
        campaign_page = buyersguide_factories.BuyersGuideCampaignPageFactory(
            parent=self.content_index,
        )
        self.bg.hero_featured_page = campaign_page
        self.bg.save()
        self.synchronize_tree()
        buyersguide_homepage_fr = self.bg.get_translation(self.fr_locale)
        campaign_page_fr = campaign_page.get_translation(self.fr_locale)
        self.activate_locale(self.fr_locale)

        result = buyersguide_homepage_fr.get_hero_featured_page()

        self.assertEqual(result, campaign_page_fr)
        self.assertEqual(type(result), BuyersGuideCampaignPage)

    def test_get_hero_supporting_pages_with_articles(self):
        articles = []
        for i in range(1, 4):
            article = buyersguide_factories.BuyersGuideArticlePageFactory(
                parent=self.content_index,
            )
            buyersguide_factories.BuyersGuidePageHeroSupportingPageRelationFactory(
                page=self.bg,
                supporting_page=article,
                sort_order=i,
            )
            articles.append(article)

        result = self.bg.get_hero_supporting_pages()

        self.assertQuerySetEqual(qs=result, values=articles)

    def test_get_hero_supporting_pages_with_campaign_pages(self):
        campaign_pages = []
        for i in range(1, 4):
            campaign = buyersguide_factories.BuyersGuideCampaignPageFactory(
                parent=self.content_index,
            )
            buyersguide_factories.BuyersGuidePageHeroSupportingPageRelationFactory(
                page=self.bg,
                supporting_page=campaign,
                sort_order=i,
            )
            campaign_pages.append(campaign)

        result = self.bg.get_hero_supporting_pages()

        self.assertQuerySetEqual(qs=result, values=campaign_pages)

    def test_get_hero_supporting_pages_with_mixed_page_types(self):
        supporting_pages = []
        for i in range(1, 4):
            if i % 2 == 0:
                page = buyersguide_factories.BuyersGuideArticlePageFactory(
                    parent=self.content_index,
                )
            else:
                page = buyersguide_factories.BuyersGuideCampaignPageFactory(
                    parent=self.content_index,
                )

            buyersguide_factories.BuyersGuidePageHeroSupportingPageRelationFactory(
                page=self.bg,
                supporting_page=page,
                sort_order=i,
            )
            supporting_pages.append(page)

        result = self.bg.get_hero_supporting_pages()

        self.assertQuerySetEqual(qs=result, values=supporting_pages)

    def test_get_hero_supporting_pages_not_set(self):
        articles = []

        result = self.bg.get_hero_supporting_pages()

        self.assertQuerySetEqual(qs=result, values=articles)

    def test_get_hero_supporting_pages_with_articles_non_default_locale(self):
        articles = []
        for i in range(1, 4):
            article = buyersguide_factories.BuyersGuideArticlePageFactory(
                parent=self.content_index,
            )
            buyersguide_factories.BuyersGuidePageHeroSupportingPageRelationFactory(
                page=self.bg,
                supporting_page=article,
                sort_order=i,
            )
            articles.append(article)
        self.synchronize_tree()
        articles_fr = [a.get_translation(self.fr_locale) for a in articles]
        buyersguide_homepage_fr = self.bg.get_translation(self.fr_locale)
        self.activate_locale(self.fr_locale)

        result = buyersguide_homepage_fr.get_hero_supporting_pages()

        self.assertQuerySetEqual(qs=result, values=articles_fr)

    def test_get_hero_supporting_pages_with_campaigns_non_default_locale(self):
        campaign_pages = []
        for i in range(1, 4):
            campaign = buyersguide_factories.BuyersGuideCampaignPageFactory(
                parent=self.content_index,
            )
            buyersguide_factories.BuyersGuidePageHeroSupportingPageRelationFactory(
                page=self.bg,
                supporting_page=campaign,
                sort_order=i,
            )
            campaign_pages.append(campaign)
        self.synchronize_tree()
        campaigns_fr = [page.get_translation(self.fr_locale) for page in campaign_pages]
        buyersguide_homepage_fr = self.bg.get_translation(self.fr_locale)
        self.activate_locale(self.fr_locale)

        result = buyersguide_homepage_fr.get_hero_supporting_pages()

        self.assertQuerySetEqual(qs=result, values=campaigns_fr)

    def test_get_hero_supporting_pages_with_mixed_page_type_non_default_locale(self):
        supporting_pages = []
        for i in range(1, 4):
            if i % 2 == 0:
                page = buyersguide_factories.BuyersGuideArticlePageFactory(
                    parent=self.content_index,
                )
            else:
                page = buyersguide_factories.BuyersGuideCampaignPageFactory(
                    parent=self.content_index,
                )
            buyersguide_factories.BuyersGuidePageHeroSupportingPageRelationFactory(
                page=self.bg,
                supporting_page=page,
                sort_order=i,
            )
            supporting_pages.append(page)

        self.synchronize_tree()
        supporting_pages_fr = [page.get_translation(self.fr_locale) for page in supporting_pages]
        buyersguide_homepage_fr = self.bg.get_translation(self.fr_locale)
        self.activate_locale(self.fr_locale)

        result = buyersguide_homepage_fr.get_hero_supporting_pages()

        self.assertQuerySetEqual(qs=result, values=supporting_pages_fr)

    def test_get_featured_articles(self):
        articles = []
        for i in range(1, 4):
            article = buyersguide_factories.BuyersGuideArticlePageFactory(
                parent=self.content_index,
            )
            buyersguide_factories.BuyersGuidePageFeaturedArticleRelationFactory(
                page=self.bg,
                article=article,
                sort_order=i,
            )
            articles.append(article)

        result = self.bg.get_featured_articles()

        self.assertQuerySetEqual(qs=result, values=articles)

    def test_get_featured_articles_not_set(self):
        articles = []

        result = self.bg.get_featured_articles()

        self.assertQuerySetEqual(qs=result, values=articles)

    def test_get_featured_articles_non_default_locale(self):
        articles = []
        for i in range(1, 4):
            article = buyersguide_factories.BuyersGuideArticlePageFactory(
                parent=self.content_index,
            )
            buyersguide_factories.BuyersGuidePageFeaturedArticleRelationFactory(
                page=self.bg,
                article=article,
                sort_order=i,
            )
            articles.append(article)
        self.synchronize_tree()
        articles_fr = [a.get_translation(self.fr_locale) for a in articles]
        buyersguide_homepage_fr = self.bg.get_translation(self.fr_locale)
        self.activate_locale(self.fr_locale)

        result = buyersguide_homepage_fr.get_featured_articles()

        self.assertQuerySetEqual(qs=result, values=articles_fr)

    def test_get_featured_advice_article(self):
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory.create(
            parent=self.content_index,
        )
        self.bg.featured_advice_article = article_page

        result = self.bg.get_featured_advice_article()

        self.assertEqual(result, article_page)

    def test_get_featured_advice_article_not_set(self):
        self.bg.featured_advice_article = None

        result = self.bg.get_featured_advice_article()

        self.assertIsNone(result)

    def test_get_featured_advice_article_non_default_locale(self):
        article_page = buyersguide_factories.BuyersGuideArticlePageFactory(
            parent=self.content_index,
        )
        self.bg.featured_advice_article = article_page
        self.bg.save()
        self.synchronize_tree()
        buyersguide_homepage_fr = self.bg.get_translation(self.fr_locale)
        article_page_fr = article_page.get_translation(self.fr_locale)
        self.activate_locale(self.fr_locale)

        result = buyersguide_homepage_fr.get_featured_advice_article()

        self.assertEqual(result, article_page_fr)
