from django.core.management import base
from wagtail import models as wagtail_models
from wagtail.actions import move_page

from networkapi.wagtailpages import models as pagemodels


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        locale_default = wagtail_models.Locale.get_default()

        buyersguidepage_default = pagemodels.BuyersGuidePage.objects.get(locale=locale_default)
        index_page_default = pagemodels.ProductIndexPage.objects.descendant_of(buyersguidepage_default).first()
        # Move all product pages from buyersguide page to index page
        for product_page in pagemodels.GeneralProductPage.objects.descendant_of(index_page_default).order_by("path"):
            print(f"Moving '{ product_page.get_url() }' to '{ buyersguidepage_default.get_url() }'")
            move = move_page.MovePageAction(page=product_page, target=buyersguidepage_default, pos="last-child")
            move.execute()

        pagemodels.ProductIndexPage.objects.all().delete()
