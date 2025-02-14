import os

from django.conf import settings
from django.core.files import File
from wagtail.images import get_image_model
from wagtail.models import Collection

TEST_IMAGE_DIR = os.path.join(settings.STATICFILES_DIRS[0], "_images", "review_app_images")
COLLECTION_NAME = "Review App Images"


def get_or_create_collection(name=COLLECTION_NAME):
    """
    Ensures the collection is created with the correct tree structure.
    """
    root_collection = Collection.get_first_root_node()
    if not root_collection:
        raise ValueError("Root collection does not exist. Ensure Wagtail migrations are applied.")

    # Check if the collection already exists
    collection = Collection.objects.filter(name=name).first()
    if collection:
        return collection

    # Create the collection properly under the root
    collection = root_collection.add_child(name=name)
    return collection


def upload_test_images():
    """Uploads all images from TEST_IMAGE_DIR to a specific Wagtail Collection."""
    Image = get_image_model()

    # Ensure collection is created correctly under the root collection
    collection = get_or_create_collection(COLLECTION_NAME)

    for image_file in os.listdir(TEST_IMAGE_DIR):
        if image_file.endswith((".jpg", ".png")):
            image_path = os.path.join(TEST_IMAGE_DIR, image_file)

            # ✅ Prevent duplicate uploads within the same collection
            if not Image.objects.filter(title=image_file, collection=collection).exists():
                with open(image_path, "rb") as img_file:
                    image_instance = Image.objects.create(
                        title=image_file, file=File(img_file, name=image_file), collection=collection
                    )
                    print(f"Uploaded: {image_instance.title} to {collection.name}")


# Run only when executed directly
if __name__ == "__main__":
    upload_test_images()
