import ntpath
import requests

from django.core.management.base import BaseCommand

from django.core.files.images import ImageFile
from io import BytesIO
from mimetypes import MimeTypes
from PIL import Image as PILImage

from wagtail.images.models import Image as WagtailImage
from networkapi.wagtailpages.pagemodels.products import ProductPage


class Command(BaseCommand):
    help = 'Migrate PNI Cloudinary images to Wagtail images'

    def handle(self, *args, **options):

        all_products = ProductPage.objects.all()
        total_products = all_products.count()

        for index, product in enumerate(all_products):
            print(f"Processing product {index+1} of {total_products}")
            if product.cloudinary_image:
                mime = MimeTypes()
                mime_type = mime.guess_type(product.cloudinary_image.url)  # -> ('image/jpeg', None)
                if mime_type:
                    mime_type = mime_type[0].split('/')[1].upper()
                else:
                    # Default to a JPEG mimetype.
                    mime_type = 'JPEG'

                # Temporarily download the image
                response = requests.get(product.cloudinary_image.url, stream=True)
                if response.status_code == 200:
                    # Create an image out of the Cloudinary URL and write it to a PIL Image.
                    pil_image = PILImage.open(response.raw)
                    f = BytesIO()
                    pil_image.save(f, mime_type)
                    # Get the file name in a nice way.
                    new_image_name = ntpath.basename(product.cloudinary_image.url)
                    # Store the image as a WagtailImage object
                    wagtail_image = WagtailImage.objects.create(
                        title=new_image_name,
                        file=ImageFile(f, name=new_image_name),
                    )
                    # Associate product.image with wagtail_image
                    product.image = wagtail_image
                    # Always generate a new revision.
                    revision = product.save_revision()
                    if product.live:
                        # Re-publish existing "live" pages from the latest revision
                        revision.publish()
