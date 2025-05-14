from factory import Faker, LazyFunction, SubFactory
from factory.django import DjangoModelFactory
from wagtail.models import Locale

from foundation_cms.legacy_apps.donate_banner.models import DonateBanner
from foundation_cms.legacy_apps.wagtailpages.factory.image_factory import ImageFactory


class DonateBannerFactory(DjangoModelFactory):
    class Meta:
        model = DonateBanner

    name = Faker("sentence", nb_words=3)
    title = Faker("sentence", nb_words=6)
    background_image = SubFactory(ImageFactory)
    locale = LazyFunction(lambda: Locale.get_default())
