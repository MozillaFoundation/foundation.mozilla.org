from django.core.management.base import BaseCommand

from networkapi.wagtailpages.pagemodels.products import ProductPage


class Command(BaseCommand):
    help = 'For new Wagtail-based PNI images: generate a usable rendition for each known image size'

    def handle(self, *args, **options):

        all_products = ProductPage.objects.all().specific()
        total_products = all_products.count()

        for i, product in enumerate(all_products):
            print(f'Processing {i+1} of {total_products}')
            if product.image:
                # Generating 9 PNI renditions for /privacynotincluded/
                product.image.get_rendition('fill-260x260')
                product.image.get_rendition('fill-520x520')
                product.image.get_rendition('fill-305x305')
                product.image.get_rendition('fill-610x610')
                product.image.get_rendition('fill-360x360')
                product.image.get_rendition('fill-720x720')
                product.image.get_rendition('fill-185x185')
                product.image.get_rendition('fill-370x370')
                product.image.get_rendition('fill-600x600')

                # Generate admin renditions for the ImageChooser and detail views
                product.image.get_rendition('max-165x165')
                product.image.get_rendition('max-800x600')
