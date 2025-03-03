import random

from django.contrib.auth import get_user_model
from django.test import RequestFactory, override_settings
from django.urls import reverse
from wagtail.models import ContentType

from foundation_cms.legacy_cms.reports.views import PageTypesReportView, _get_locale_choices
from foundation_cms.legacy_cms.wagtailpages.factory.buyersguide import ProductPageFactory
from foundation_cms.legacy_cms.wagtailpages.factory.profiles import ProfileFactory
from foundation_cms.legacy_cms.wagtailpages.models import Homepage, ProductPage, Profile
from foundation_cms.legacy_cms.wagtailpages.tests.base import WagtailpagesTestCase


class PageTypesReportViewTest(WagtailpagesTestCase):
    def setUp(self):
        super().setUp()
        self.view = PageTypesReportView()
        self.view.request = RequestFactory().get(reverse("page_types_report"))

    def test_queryset_filtering(self):
        """Asserts that the correct models are included in the queryset."""
        # Create some pages from different content types
        ProductPageFactory()
        ProductPageFactory()
        # Create a non-page model
        ProfileFactory()
        # Test that the queryset is correctly filtered by page models
        queryset = self.view.get_queryset()
        # Assert that the queryset contains the correct page models
        self.assertIn(ContentType.objects.get_for_model(Homepage), queryset)
        self.assertIn(ContentType.objects.get_for_model(ProductPage), queryset)
        # Assert that the queryset does not contain the non-page model
        self.assertNotIn(ContentType.objects.get_for_model(Profile), queryset)

    def test_queryset_ordering(self):
        """Asserts that the queryset is ordered by page model count."""
        # Create some pages from different content types
        ProductPageFactory()
        ProductPageFactory()
        ProductPageFactory()
        # Test that the queryset is correctly ordered by page model count
        queryset = self.view.get_queryset()
        # Convert queryset to list of ids to make it easier to test
        queryset_list_pks = list(queryset.values_list("pk", flat=True))
        # Get the positions of the content types in the list
        product_page_content_type = ContentType.objects.get_for_model(ProductPage)
        product_page_position = queryset_list_pks.index(product_page_content_type.pk)
        homepage_content_type = ContentType.objects.get_for_model(Homepage)
        homepage_position = queryset_list_pks.index(homepage_content_type.pk)
        # Assert that the ProductPage comes before Homepage, since it has more entries
        self.assertTrue(product_page_position < homepage_position)
        # Assert entry counts
        self.assertEqual(queryset.get(id=product_page_content_type.pk).count, 3)
        self.assertEqual(queryset.get(id=homepage_content_type.pk).count, 1)

    def test_queryset_last_edited_page(self):
        """Tests that the queryset correctly returns the last edited page."""
        # Create some product pages:
        product_page_a = ProductPageFactory(parent=self.homepage)
        product_page_b = ProductPageFactory(parent=self.homepage)
        product_page_c = ProductPageFactory(parent=self.homepage)
        # Edit the first product page
        revision = product_page_a.save_revision()
        revision.publish()
        # Edit the second product page
        revision = product_page_b.save_revision()
        revision.publish()
        # Edit the third product page
        revision = product_page_c.save_revision()
        revision.publish()
        # Re-edit the first product page
        revision = product_page_a.save_revision()
        revision.publish()
        # Get the queryset:
        queryset = self.view.decorate_paginated_queryset(self.view.get_queryset())
        # Assert that the first product page is the last edited page
        product_page_a.refresh_from_db()
        self.assertEqual(queryset[0].last_edited_page.id, product_page_a.id)

    def test_queryset_last_edited_by(self):
        """Tests that the queryset correctly returns the last edited by user."""
        # Create some product pages:
        product_page_a = ProductPageFactory(parent=self.homepage)
        ProductPageFactory(parent=self.homepage)
        ProductPageFactory(parent=self.homepage)
        # Create some users:
        user_a = self.create_superuser(username="user_a", first_name="John", last_name="Doe")
        user_b = self.create_superuser(username="user_b", first_name="Jane", last_name="Doe")
        # Edit the first product page with user_a
        revision = product_page_a.save_revision(user=user_a)
        revision.publish(user=user_a)
        # Re-edit the first product page with user_b
        revision = product_page_a.save_revision(user=user_b)
        revision.publish(user=user_b)
        # Get the queryset:
        queryset = self.view.decorate_paginated_queryset(self.view.get_queryset())
        # Assert that the first product page is the last edited page
        product_page_a.refresh_from_db()
        self.assertEqual(queryset[0].last_edited_page.id, product_page_a.id)
        # Assert that the first product page was last edited by user b
        self.assertEqual(queryset[0].last_edited_by, user_b.id)
        self.assertEqual(queryset[0].last_edited_by_user, user_b.get_username())


class PageTypesReportFiltersTests(WagtailpagesTestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser("admin-user", "admin@example.com", "password")
        self.client.force_login(self.user)

    def test_all_locales_shown_if_no_filter(self):
        """Tests that all locales are shown if no filter is applied."""
        # Create a product page in default locale
        product_page = ProductPageFactory(parent=self.homepage)
        # Activate French locale
        self.activate_locale(self.fr_locale)
        # Translate pages to French
        self.homepage.copy_for_translation(self.fr_locale)
        product_page.copy_for_translation(self.fr_locale)

        # Edit the product page in English to make sure that it's the latest
        product_page.title = "Updated English title"
        revision = product_page.save_revision()
        product_page.publish(revision)

        response = self.client.get(reverse("page_types_report"))
        page_types = {content_type.id: content_type for content_type in response.context["object_list"]}

        homepage_row = page_types.get(ContentType.objects.get_for_model(Homepage).pk)
        productpage_row = page_types.get(ContentType.objects.get_for_model(ProductPage).pk)

        # There should be 2 of each page (one for each locale)
        self.assertEqual(homepage_row.count, 2)
        self.assertEqual(productpage_row.count, 2)
        # The last edited page should be the French version
        self.assertEqual(homepage_row.last_edited_page.locale, self.fr_locale)
        self.assertEqual(productpage_row.last_edited_page.locale, self.default_locale)

    def test_all_locales_shown_if_show_all(self):
        """Tests that all locales are shown if the null/show all filter is applied."""
        # Create a product page in default locale
        product_page = ProductPageFactory(parent=self.homepage)
        # Activate French locale
        self.activate_locale(self.fr_locale)
        # Translate pages to French
        self.homepage.copy_for_translation(self.fr_locale)
        product_page.copy_for_translation(self.fr_locale)

        # Edit the product page in English to make sure that it's the latest
        product_page.title = "Updated English title"
        revision = product_page.save_revision()
        product_page.publish(revision)

        empty_value = random.choice(("", "all"))

        response = self.client.get(reverse("page_types_report"), data={"page_locale": empty_value})
        page_types = {content_type.id: content_type for content_type in response.context["object_list"]}

        homepage_row = page_types.get(ContentType.objects.get_for_model(Homepage).pk)
        productpage_row = page_types.get(ContentType.objects.get_for_model(ProductPage).pk)

        # There should be 2 of each page (one for each locale)
        self.assertEqual(homepage_row.count, 2)
        self.assertEqual(productpage_row.count, 2)
        # The last edited page should be the French version
        self.assertEqual(homepage_row.last_edited_page.locale, self.fr_locale)
        self.assertEqual(productpage_row.last_edited_page.locale, self.default_locale)

    def test_filter_by_locale(self):
        """Tests that the queryset is filtered by locale."""
        # Create a product page in default locale
        product_page = ProductPageFactory(parent=self.homepage)
        # Activate French locale
        self.activate_locale(self.fr_locale)
        # Translate pages to French
        self.homepage.copy_for_translation(self.fr_locale)
        product_page.copy_for_translation(self.fr_locale)

        # Edit the product page in English to make sure that it's the latest
        product_page.title = "Updated English title"
        revision = product_page.save_revision()
        product_page.publish(revision)

        response = self.client.get(reverse("page_types_report"), data={"page_locale": self.fr_locale.language_code})
        page_types = {content_type.id: content_type for content_type in response.context["object_list"]}

        homepage_row = page_types.get(ContentType.objects.get_for_model(Homepage).pk)
        productpage_row = page_types.get(ContentType.objects.get_for_model(ProductPage).pk)

        # There should be 1 of each page (only the French locale ones)
        self.assertEqual(homepage_row.count, 1)
        self.assertEqual(productpage_row.count, 1)
        # The last edited page should be the French version (even though product page was later edited in English)
        self.assertEqual(homepage_row.last_edited_page.locale, self.fr_locale)
        self.assertEqual(productpage_row.last_edited_page.locale, self.fr_locale)

    @override_settings(
        LANGUAGE_CODE="en", WAGTAIL_CONTENT_LANGUAGES=[("en", "English"), ("de", "German"), ("fr", "French")]
    )
    def test_get_locale_choices(self):
        choices = _get_locale_choices()

        expected_choices = [
            ("en", "English"),
            ("de", "German"),
            ("fr", "French"),
        ]

        self.assertCountEqual(choices, expected_choices)
