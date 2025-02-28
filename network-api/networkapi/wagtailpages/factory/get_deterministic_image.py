import random

from wagtail.images.models import Image
from wagtail.models import Collection

from networkapi.wagtailpages.factory.upload_review_app_images import (
    upload_review_app_images,
)

COLLECTION_NAME = "Review App Images"


def get_deterministic_image(reference_value, collection_name=COLLECTION_NAME):
    """
    Selects a random image deterministically based on a reference value.
    Ensures images exist before selecting one.

    :param reference_value: A stable reference (e.g., title) to ensure the same image is picked each time.
    :param collection_name: Optional name of a Wagtail image collection to filter images.
    :return: A Wagtail Image instance.
    """

    print(f">>> !!!!!!!!!! Available collections in CI: {list(Collection.objects.all().values_list('name', flat=True))}")

    # When reference_value is None, hash(reference_value) will return different values between runs
    if reference_value is None:
        raise ValueError("reference_value cannot be None")

    # Ensure images exist before selecting
    if not Image.objects.exists():
        print(">>> Running upload_review_app_images() to populate images...")
        upload_review_app_images()
        print(f">>> After upload: {Image.objects.count()} images exist in Wagtail.")

    if not collection_name:
        raise ValueError(">>>> collection_name is empty or None before filtering images!")

    images = Image.objects.all()
    if collection_name:
        images = images.filter(collection__name=collection_name)

    images = list(images)
    if not images:
        raise ValueError(f'No images found in collection "{collection_name}" ')

    # Use a deterministic random selection based on `reference_value`
    stable_random = random.Random(hash(reference_value))

    return stable_random.choice(images)
