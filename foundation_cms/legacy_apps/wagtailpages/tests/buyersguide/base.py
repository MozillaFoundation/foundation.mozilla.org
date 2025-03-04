from os.path import abspath, join

from django.conf import settings
from django.test.utils import override_settings

from foundation_cms.legacy_apps.wagtailpages.pagemodels.buyersguide.homepage import (
    BuyersGuidePage,
)
from foundation_cms.legacy_apps.wagtailpages.pagemodels.buyersguide.products import (
    ProductPage,
    ProductPageEvaluation,
)
from foundation_cms.legacy_apps.wagtailpages.tests import base as test_base
from foundation_cms.legacy_apps.wagtailpages.utils import create_wagtail_image


@override_settings(CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}})
class BuyersGuideTestCase(test_base.WagtailpagesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # Ensure there's always a BuyersGuide Page
        cls.bg = cls.get_or_create_buyers_guide()
        cls.product_page = cls.get_or_create_product_page()

    @classmethod
    def get_or_create_buyers_guide(cls):
        """
        Return the first BuyersGuidePage, or create a new one.
        Will generate a Homepage if needed.
        """
        buyersguide = BuyersGuidePage.objects.first()
        if not buyersguide:
            # Create the buyersguide page.
            buyersguide = BuyersGuidePage(locale=cls.default_locale)
            buyersguide.title = "Privacy not included"
            buyersguide.slug = "privacynotincluded"
            cls.homepage.add_child(instance=buyersguide)
            buyersguide.save_revision().publish()
        return buyersguide

    @classmethod
    def get_or_create_product_page(cls):
        product_page = ProductPage.objects.first()
        if not product_page:
            image_path = abspath(
                join(
                    settings.BASE_DIR,
                    "media/images/placeholders/products/babymonitor.jpg",
                )
            )
            wagtail_image = create_wagtail_image(image_path, collection_name="pni products")
            product_page = ProductPage(
                slug="product-page",
                title="Product Page",
                live=True,
                image=wagtail_image,
                locale=cls.default_locale,
            )
            cls.bg.add_child(instance=product_page)
            product_page.save_revision().publish()
        # Reset votes:
        product_page.evaluation = ProductPageEvaluation.objects.create()
        product_page.save()
        return product_page
