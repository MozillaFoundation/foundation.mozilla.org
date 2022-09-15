from os.path import abspath, join

from django.conf import settings
from django.test.utils import override_settings

from networkapi.wagtailpages.factory.homepage import WagtailHomepageFactory
from networkapi.wagtailpages.pagemodels.base import Homepage
from networkapi.wagtailpages.pagemodels.buyersguide.homepage import BuyersGuidePage
from networkapi.wagtailpages.pagemodels.buyersguide.products import (
    ProductPage,
)
from networkapi.wagtailpages.utils import create_wagtail_image

from wagtail.core.models import Page, Site
from wagtail.tests.utils import WagtailPageTests


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
class BuyersGuideTestMixin(WagtailPageTests):

    def setUp(self):
        # Ensure there's always a BuyersGuide Page
        self.bg = self.get_or_create_buyers_guide()
        self.product_page = self.get_or_create_product_page()

        site = Site.objects.first()
        site.root_page = self.homepage
        site.save()

    def get_or_create_buyers_guide(self):
        """
        Return the first BuyersGuidePage, or create a new one.
        Will generate a Homepage if needed.
        """
        buyersguide = BuyersGuidePage.objects.first()
        if not buyersguide:
            homepage = Homepage.objects.first()
            if not homepage:
                page_tree_root = Page.objects.get(depth=1)
                homepage = WagtailHomepageFactory.create(
                    parent=page_tree_root,
                    title='Homepage',
                    slug='homepage',
                    hero_image__file__width=1080,
                    hero_image__file__height=720
                )
            # Create the buyersguide page.
            buyersguide = BuyersGuidePage()
            buyersguide.title = 'Privacy not included'
            buyersguide.slug = 'privacynotincluded'
            homepage.add_child(instance=buyersguide)
            buyersguide.save_revision().publish()
        self.homepage = Homepage.objects.first()
        return buyersguide

    def get_or_create_product_page(self):
        product_page = ProductPage.objects.first()
        if not product_page:
            image_path = abspath(join(
                settings.BASE_DIR,
                'media/images/placeholders/products/babymonitor.jpg',
            ))
            wagtail_image = create_wagtail_image(
                image_path,
                collection_name='pni products'
            )
            product_page = ProductPage(
                slug='product-page',
                title='Product Page',
                live=True,
                image=wagtail_image
            )
            self.bg.add_child(instance=product_page)
            product_page.save_revision().publish()
        return product_page
