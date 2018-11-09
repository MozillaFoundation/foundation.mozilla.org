from random import choices, randint

from django.conf import settings
from faker.providers import BaseProvider


# Used to return a random number of tags, issues or helptypes to associate with fake pulse entries or profile
def get_random_items(model):
    items = model.objects.all()
    return choices(items, k=randint(0, len(items)))


class ImageProvider(BaseProvider):
    """
    A custom Faker Provider for relative image urls, for use with factory_boy

    >>> from factory import Faker
    >>> from networkapi.utility.faker_providers import ImageProvider
    >>> fake - Faker()
    >>> Faker.add_provider(ImageProvider)
    """

    if settings.USE_CLOUDINARY:
        base_path = 'foundationsite/images/placeholders/'
    else:
        base_path = 'images/placeholders/'

    generic_images = (
        'generic/tigerparrot.jpg',
        'generic/photographer.jpg',
        'generic/windfarm.jpg',
        'generic/hotair.jpg',
        'generic/computerandcoffee.jpg',
    )

    headshot_images = (
        'people/woman.jpg',
        'people/man.jpg',
        'people/dino.jpg',
    )

    def generic_image(self):
        """
        returns a path to one of the predefined generic placeholder images
        """

        return '{}{}'.format(self.base_path, self.random_element(self.generic_images))

    def people_image(self):
        """
        returns a path to one of the predefined people placeholder images
        """

        return '{}{}'.format(self.base_path, self.random_element(self.headshot_images))
