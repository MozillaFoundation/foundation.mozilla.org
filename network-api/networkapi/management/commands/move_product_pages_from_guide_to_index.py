from django.core.management import base
from wagtail import models as wagtail_models
from wagtail.actions import move_page

from networkapi.wagtailpages import models as pagemodels


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        # In default locale
        locale_default = wagtail_models.Locale.get_default()
        # Create index page under buyersguide page
        buyersguidepage_default = pagemodels.BuyersGuidePage.objects.get(locale=locale_default)
        try:
            index_page_default = pagemodels.ProductIndexPage.objects.get(locale=locale_default)
        except pagemodels.ProductIndexPage.DoesNotExist:
            index_page_default = pagemodels.ProductIndexPage(
                title="Product reviews",
                slug="product-reviews",
                locale=locale_default,
            )
            buyersguidepage_default.add_child(instance=index_page_default)
            index_page_default.save_revision().publish()
        # Move all product pages from buyersguide page to index page
        for product_page in pagemodels.GeneralProductPage.objects.descendant_of(buyersguidepage_default).order_by("path")[:10]:
            print(f"Moving '{ product_page.get_url() }' to '{ index_page_default.get_url() }'")
            move = move_page.MovePageAction(page=product_page, target=index_page_default, pos="last-child")
            move.execute()


        # For all buyersguide pages not in default locale
        # Create copy of index page for translation in the locale
        # Move all product pages from the buyersguide page of the locale to the index page of the locale
