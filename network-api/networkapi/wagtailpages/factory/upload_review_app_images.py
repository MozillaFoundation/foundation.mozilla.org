import os

from django.conf import settings
from django.core.files import File
from wagtail.images import get_image_model
from wagtail.models import Collection

if os.getenv("DOCKER_ENV"):
    IMAGE_DIR = "/app/network-api/networkapi/frontend/_images/review_app_images"
else:
    IMAGE_DIR = os.path.join(settings.BASE_DIR, "networkapi/frontend/_images/review_app_images")

print(f"📂 Using IMAGE_DIR: {IMAGE_DIR}")


COLLECTION_NAME = "Review App Images"


def get_or_create_collection(name=COLLECTION_NAME):
    """
    Ensures the collection is created under the correct root node.
    """

    # Debug: Show existing collections
    existing_collections = list(Collection.objects.all().values_list("name", flat=True))
    print(f"🔍 Existing collections before creation: {existing_collections}")

    # Get the root collection
    root_collection = Collection.get_first_root_node()
    if not root_collection:
        print(">>> Root collection is missing! Creating it manually...")
        root_collection = Collection.add_root(name="Root")

    # Check if the collection already exists
    collection = Collection.objects.filter(name=name).first()
    if collection:
        print(f">>> Collection '{name}' already exists.")
        return collection

    # Correctly create the collection under the root
    collection = root_collection.add_child(name=name)
    print(f">>>> Created new collection: {name} under {root_collection.name}")

    return collection


def upload_review_app_images():
    """Uploads all images from IMAGE_DIR to a specific Wagtail Collection."""
    Image = get_image_model()

    print(f"📂 Checking IMAGE_DIR: {IMAGE_DIR}")

    # Ensure IMAGE_DIR exists (prevents errors in CI)
    if not os.path.exists(IMAGE_DIR):
        print(f">>> ERROR: IMAGE_DIR '{IMAGE_DIR}' does not exist! Creating it...")
        os.makedirs(IMAGE_DIR, exist_ok=True)
        return  # If the directory was just created, no images exist yet.

    # List all files in IMAGE_DIR
    all_files = os.listdir(IMAGE_DIR)
    print(f">>> Found {len(all_files)} files in IMAGE_DIR.")

    # ✅ Filter only images (JPG, PNG)
    image_files = [f for f in all_files if f.lower().endswith((".jpg", ".png"))]
    print(f">>> Found {len(image_files)} image files.")

    if not image_files:
        print("⚠️ No image files found in IMAGE_DIR. Exiting.")
        return

    # Ensure collection is created correctly under the root collection
    collection = get_or_create_collection(COLLECTION_NAME)

    # Handle the case where `get_or_create_collection` fails
    if not collection:
        print(f"❌ ERROR: Collection '{COLLECTION_NAME}' could not be created!")
        return

    print(f"📂 Using collection: {collection.name}")

    uploaded_count = 0

    for image_file in image_files:
        image_path = os.path.join(IMAGE_DIR, image_file)

        # Ensure image file exists before opening
        if not os.path.exists(image_path):
            print(f"⚠️ Skipping: {image_file} (File not found)")
            continue

        print(f">>>  Processing: {image_file}")

        # Prevent duplicate uploads within the same collection
        if Image.objects.filter(title=image_file, collection=collection).exists():
            print(f">>>  Skipping: {image_file} (Already Exists)")
            continue

        try:
            with open(image_path, "rb") as img_file:
                image_instance = Image.objects.create(
                    title=image_file, file=File(img_file, name=image_file), collection=collection
                )
                uploaded_count += 1
                print(f">>> Uploaded: {image_instance.title} to {collection.name}")

            # Ensure the image was actually saved in the database
            assert Image.objects.filter(
                title=image_file, collection=collection
            ).exists(), f">>>  ERROR: Image {image_file} was not saved correctly!"

        except Exception as e:
            print(f">>>  ERROR: Failed to upload {image_file}. Reason: {e}")

    print(f">>>  Successfully uploaded {uploaded_count} new images.")


# Run only when executed directly
if __name__ == "__main__":
    upload_review_app_images()
