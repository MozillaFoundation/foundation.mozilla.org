from cloudinary.models import CloudinaryField


# Override the default 'public_id' to upload all images to the buyers guide directory on Cloudinary
# TODO: this is not needed anymore and needs to be removed.
class CloudinaryImageField(CloudinaryField):
    def upload_options(self, model_instance):
        return {
            'folder': 'foundationsite/buyersguide',
            'use_filename': True,
        }
