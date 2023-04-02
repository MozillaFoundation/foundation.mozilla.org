import factory

from networkapi.wagtailpages import models as wagtailpage_models


class ResearchRegionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.ResearchRegion

    name = factory.Faker("text", max_nb_chars=25)


class ResearchTopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.ResearchTopic

    name = factory.Faker("text", max_nb_chars=25)
    description = factory.Faker("paragraph")
