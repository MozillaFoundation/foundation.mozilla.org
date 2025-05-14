import factory
from django.utils import text as text_utils

from foundation_cms.legacy_apps.wagtailpages import models as wagtailpage_models


class RCCBaseTaxonomyFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    name = factory.Faker("text", max_nb_chars=25)

    @factory.post_generation
    def set_slug(obj, created, extracted, **kwargs):
        obj.slug = text_utils.slugify(obj.name)


class RCCContentTypeFactory(RCCBaseTaxonomyFactory):
    class Meta:
        model = wagtailpage_models.RCCContentType


class RCCCurricularAreaFactory(RCCBaseTaxonomyFactory):
    class Meta:
        model = wagtailpage_models.RCCCurricularArea


class RCCTopicFactory(RCCBaseTaxonomyFactory):
    class Meta:
        model = wagtailpage_models.RCCTopic
