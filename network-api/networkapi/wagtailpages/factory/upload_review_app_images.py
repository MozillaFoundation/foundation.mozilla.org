import os

from django.conf import settings
from django.core.files import File
from wagtail.images import get_image_model
from wagtail.models import Collection

IMAGE_DIR = os.path.join(settings.STATICFILES_DIRS[0], "_images", "review_app_images")
COLLECTION_NAME = "Review App Images"


def get_or_create_collection(name=COLLECTION_NAME):
    """
    Ensures the collection is created with the correct tree structure.
    """
    if not Collection.objects.exists():
        return None  # Avoids querying an uninitialized test database

    root_collection = Collection.get_first_root_node()

    # Check if the collection already exists
    collection = Collection.objects.filter(name=name).first()
    if collection:
        return collection

    # Create the collection properly under the root
    collection = root_collection.add_child(name=name)
    return collection


def upload_review_app_images():
    """Uploads all images from IMAGE_DIR to a specific Wagtail Collection."""
    Image = get_image_model()

    print(f"📂 Checking IMAGE_DIR: {IMAGE_DIR}")

    # for debugging...
    # Check if IMAGE_DIR exists
    if not os.path.exists(IMAGE_DIR):
        print(f">>> ERROR: IMAGE_DIR '{IMAGE_DIR}' does not exist!")
        return

    # for debugging...
    # List all files in IMAGE_DIR
    all_files = os.listdir(IMAGE_DIR)
    print(f">>> Found {len(all_files)} files in IMAGE_DIR.")

    # for debugging...
    # Filter only images (JPG, PNG)
    image_files = [f for f in all_files if f.lower().endswith((".jpg", ".png"))]
    print(f">>> Found {len(image_files)} image files.")

    if not image_files:
        print(">>> No image files found in IMAGE_DIR. Exiting.")
        return

    # Ensure collection is created correctly under the root collection
    collection = get_or_create_collection(COLLECTION_NAME)

    uploaded_count = 0

    for image_file in image_files:
        image_path = os.path.join(IMAGE_DIR, image_file)
        print(f"Processing: {image_file}")

        # Prevent duplicate uploads within the same collection
        if Image.objects.filter(title=image_file, collection=collection).exists():
            print(f"Skipping: {image_file} (Already Exists)")
            continue

        with open(image_path, "rb") as img_file:
            image_instance = Image.objects.create(
                title=image_file, file=File(img_file, name=image_file), collection=collection
            )
            uploaded_count += 1
            print(f"Uploaded: {image_instance.title} to {collection.name}")

    print(f"Successfully uploaded {uploaded_count} new images.")


# Run only when executed directly
if __name__ == "__main__":
    upload_review_app_images()
