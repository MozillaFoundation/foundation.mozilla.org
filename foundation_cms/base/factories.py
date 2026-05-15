import factory
from django.utils.text import slugify
from factory.django import DjangoModelFactory, ImageField
from wagtail.images import get_image_model
from wagtail.models import Collection

from foundation_cms.base.models.abstract_base_page import Topic

IMAGE_COLORS = ["red", "blue", "green", "purple", "pink"]


class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = Collection
        django_get_or_create = ("name",)

    name = "Root"


class CollectionMemberFactory(DjangoModelFactory):
    collection = factory.SubFactory(CollectionFactory)


class ImageFactory(CollectionMemberFactory):
    """
    Custom image factory that places all images in the Root collection.
    """

    class Meta:
        model = get_image_model()

    title = "An image"
    file = ImageField()


TOPIC_NAMES = [
    "Artificial Intelligence",
    "Privacy",
    "Security",
    "Open Web",
    "Democracy",
    "Health",
    "Education",
    "Environment",
    "Human Rights",
    "Media",
]


def generate_images():
    images = []
    for color in IMAGE_COLORS * 4:
        images.append(ImageFactory.create(file__color=color))
    return images


def generate_topics():
    topics = []
    for name in TOPIC_NAMES:
        topic, _ = Topic.objects.get_or_create(
            slug=slugify(name),
            defaults={"name": name},
        )
        topics.append(topic)
    return topics
