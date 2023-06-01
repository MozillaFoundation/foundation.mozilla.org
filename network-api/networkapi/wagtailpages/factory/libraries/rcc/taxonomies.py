import factory
from django.utils import text as text_utils

from networkapi.wagtailpages import models as wagtailpage_models


class RCCContentTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.RCCContentType

    name = factory.Faker("text", max_nb_chars=25)

    @factory.post_generation
    def set_slug(obj, created, extracted, **kwargs):
        obj.slug = text_utils.slugify(obj.name)


class RCCCurricularAreaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.RCCCurricularArea

    name = factory.Faker("text", max_nb_chars=25)

    @factory.post_generation
    def set_slug(obj, created, extracted, **kwargs):
        obj.slug = text_utils.slugify(obj.name)


class RCCTopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.RCCTopic

    name = factory.Faker("text", max_nb_chars=25)

    @factory.post_generation
    def set_slug(obj, created, extracted, **kwargs):
        obj.slug = text_utils.slugify(obj.name)
