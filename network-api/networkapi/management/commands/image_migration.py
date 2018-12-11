from django.core.files.uploadedfile import UploadedFile
from django.core.management.base import BaseCommand

from networkapi.buyersguide.models import Product


class Command(BaseCommand):
    help = 'Migrate BuyersGuide images from s3 to Cloudinary'

    def handle(self, *args, **options):

        all_products = Product.objects.all()

        for product in all_products:
            if product.image:
                image = UploadedFile(product.image.file, product.image.file.name)
                product.cloudinary_image = image
                product.save()
                print(f"Product image for {product.name} migrated")
            else:
                print(f"No Product image for {product.name} to migrate")
