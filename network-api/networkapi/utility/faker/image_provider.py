from faker.providers import BaseProvider


# FIXME: this code doesn't work at all, probably due to major version updates,
#        and this ImageProvider is basically dead code by now.
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

    product_images = (
        'products/drone.jpg',
        'products/echo.jpg',
        'products/nest.jpg',
        'products/babymonitor.jpg',
        'products/teddy.jpg'
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

    def product_image(self):
        """
        returns a path to one of the predefined product placeholder images
        """

        return '{}{}'.format(self.base_path, self.random_element(self.product_images))
