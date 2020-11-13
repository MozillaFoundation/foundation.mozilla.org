import ntpath
from io import BytesIO
from mimetypes import MimeTypes
from PIL import Image as PILImage

from django.core.files.images import ImageFile
from django.db.migrations.operations.models import ModelOperation
from networkapi.utility.images import get_image_upload_path


def get_category_og_image_upload_path(instance, filename):
    return get_image_upload_path(
        app_name='buyersguide',
        prop_name='name',
        instance=instance,
        current_filename=filename
    )

from wagtail.images.models import Image as WagtailImage

from networkapi.buyersguide.pagemodels.products.base import Product
from networkapi.wagtailpages.pagemodels.products import ProductPage


def tri_to_quad(input):
    if input is True:
        return 'Yes'
    if input is False:
        return 'No'
    return 'U'


def quad_to_tri(input):
    if input == 'Yes':
        return True
    if input == 'No':
        return False
    return None


class AlterModelBases(ModelOperation):
    """
    See https://stackoverflow.com/a/61723620/740553
    """

    reduce_to_sql = False
    reversible = True

    def __init__(self, name, bases):
        self.bases = bases
        super().__init__(name)

    def state_forwards(self, app_label, state):
        state.models[app_label, self.name_lower].bases = self.bases
        state.reload_model(app_label, self.name_lower)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        pass

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        pass

    def describe(self):
        return "Update %s bases to %s" % (self.name, self.bases)


def convert_pni_file_to_product_page_image(pni_product: Product, new_product_page: ProductPage):
    """
    Take an existing product and convert it's FileField image to a WagtailImage object.

    pni_product must be an instance of a Product
    new_product_page must be an instance of a ProductPage
    """
    # 1. Get the mimetype of the image.
    mime = MimeTypes()
    mime_type = mime.guess_type(pni_product.image.file.name)  # -> ('image/jpeg', None)
    if mime_type:
        mime_type = mime_type[0].split('/')[1].upper()
    else:
        # Default to a JPEG mimetype.
        mime_type = 'JPEG'

    # 2. Create an image out of the FileField.
    pil_image = PILImage.open(pni_product.image.file)
    f = BytesIO()
    pil_image.save(f, mime_type)

    new_image_name = ntpath.basename(pni_product.image.file.name)
    wagtail_image = WagtailImage.objects.create(
        title=new_image_name,
        file=ImageFile(f, name=new_image_name)
    )

    # 3. Associate new_product_page.image with wagtail_image
    new_product_page.image = wagtail_image

    # Don't save the page in case it's still being worked on. Simply return it.
    return new_product_page
