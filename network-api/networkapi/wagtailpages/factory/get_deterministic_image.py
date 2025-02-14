import random

from wagtail.images.models import Image

COLLECTION_NAME = "Review App Images"


def get_deterministic_image(reference_value, collection_name=COLLECTION_NAME):
    """
    Selects a random image deterministically based on a reference value.

    :param reference_value: A stable reference (e.g., title) to ensure the same image is picked each time.
    :param collection_name: Optional name of a Wagtail image collection to filter images.
    :return: A Wagtail Image instance.
    """

    images = Image.objects.all()
    if collection_name:
        images = images.filter(collection__name=collection_name)

    images = list(images)
    if not images:
        raise ValueError(f"No images found{f' in collection {collection_name}' if collection_name else ''}.")

    # Use a deterministic random selection based on `reference_value`
    stable_random = random.Random(hash(reference_value))

    return stable_random.choice(images)
