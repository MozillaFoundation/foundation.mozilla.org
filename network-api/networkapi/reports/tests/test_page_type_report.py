from wagtail.models import ContentType

from networkapi.reports.views import PageTypesReportView
from networkapi.wagtailpages.factory.buyersguide import ProductPageFactory
from networkapi.wagtailpages.factory.profiles import ProfileFactory
from networkapi.wagtailpages.models import Homepage, ProductPage, Profile
from networkapi.wagtailpages.tests.base import WagtailpagesTestCase


class PageTypesReportViewTest(WagtailpagesTestCase):
    def setUp(self):
        super().setUp()
        self.view = PageTypesReportView()

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
