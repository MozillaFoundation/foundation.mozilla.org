from faker.providers import BaseProvider


class ImageProvider(BaseProvider):
    """
    A custom Faker Provider for relative image urls, for use with factory_boy

    >>> from factory import Faker
    >>> from networkapi.utility.faker import ImageProvider
    >>> fake = Faker()
    >>> Faker.add_provider(ImageProvider)
    """

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
