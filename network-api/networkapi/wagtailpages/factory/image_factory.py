import factory
from factory.django import DjangoModelFactory, ImageField
from wagtail.images import get_image_model
from wagtail.models import Collection

# Slightly modify the wagtail_factories ImageFactory so that it
# always generates images in the Root collection:


class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = Collection
        django_get_or_create = ("name",)

    name = "Root"


class CollectionMemberFactory(DjangoModelFactory):
    collection = factory.SubFactory(CollectionFactory)


class ImageFactory(CollectionMemberFactory):
    """
    Custom image factory that is almost exactly like the default image
    factory, except all images are part of the Root collection, rather
    than each image being its own collection.
    """

    class Meta:
        model = get_image_model()

    title = "An image"
    file = ImageField()
