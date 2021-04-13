from django.core.management.base import BaseCommand

from networkapi.wagtailpages.pagemodels.products import ProductUpdates, Update as NewUpdate
from networkapi.buyersguide.pagemodels.product_update import Update as OldUpdate


class Command(BaseCommand):
    help = '''
        Copies the old BuyersGuide Update data to the Wagtailpages Update model and
        updates the Orderable data in ProductUpdates
    '''

    def handle(self, *args, **options):
        all_old_products = OldUpdate.objects.all()
        total_old_products = all_old_products.count()
        print("Total products to update:", total_old_products)

        print("Deleting new products for a clean migrations...")
        NewUpdate.objects.all().delete()

        for i, old_update in enumerate(all_old_products):
            # Progress update
            print(f"Copying item {i+1} out of {total_old_products}")

            # Create a new update with the old data
            new_update = NewUpdate.objects.create(
                source=old_update.source,
                title=old_update.title,
                author=old_update.author,
                featured=old_update.featured,
                snippet=old_update.snippet,
                created_date=old_update.created_date,
            )

            # Find any ProductUpdates that use the old update.
            # If any are found, loop through them and update the `update_new` field with
            # the `new_update` object from object.
            related_product_updates = ProductUpdates.objects.filter(update=old_update)
            total_related_product_updates = related_product_updates.count()
            print("\tLooking for ProductUpdates to update. Found:", total_related_product_updates)
            for product_update in related_product_updates:
                print(f"\tUpdating related product {i+1} out of {total_related_product_updates}")
                product_update.update_new = new_update
                product_update.save()
