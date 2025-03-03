import factory
from django.utils import text as text_utils

from foundation_cms.legacy_cms.wagtailpages import models as wagtailpage_models


class ResearchRegionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.ResearchRegion

    name = factory.Faker("text", max_nb_chars=25)

    @factory.post_generation
    def set_slug(obj, created, extracted, **kwargs):
        obj.slug = text_utils.slugify(obj.name)


class ResearchTopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.ResearchTopic

    name = factory.Faker("text", max_nb_chars=25)
    description = factory.Faker("paragraph")

    @factory.post_generation
    def set_slug(obj, created, extracted, **kwargs):
        obj.slug = text_utils.slugify(obj.name)
