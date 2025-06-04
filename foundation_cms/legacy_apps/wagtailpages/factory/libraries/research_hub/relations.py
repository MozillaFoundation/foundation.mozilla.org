import factory

from foundation_cms.legacy_apps.wagtailpages import models as wagtailpage_models
from foundation_cms.legacy_apps.wagtailpages.factory import profiles as profiles_factory
from foundation_cms.legacy_apps.wagtailpages.factory.libraries.research_hub import (
    detail_page as detail_page_factory,
)
from foundation_cms.legacy_apps.wagtailpages.factory.libraries.research_hub import (
    landing_page as landing_page_factory,
)
from foundation_cms.legacy_apps.wagtailpages.factory.libraries.research_hub import (
    taxonomies as taxonomies_factory,
)


class ResearchAuthorRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.ResearchAuthorRelation

    detail_page = factory.SubFactory(detail_page_factory.ResearchDetailPageFactory)
    author_profile = factory.SubFactory(profiles_factory.ProfileFactory)


class ResearchLandingPageFeaturedAuthorsRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.ResearchLandingPageFeaturedAuthorsRelation

    landing_page = factory.SubFactory(landing_page_factory.ResearchLandingPageFactory)
    author = factory.SubFactory(profiles_factory.ProfileFactory)


class ResearchDetailPageResearchRegionRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.ResearchDetailPageResearchRegionRelation

    detail_page = factory.SubFactory(detail_page_factory.ResearchDetailPageFactory)
    region = factory.SubFactory(taxonomies_factory.ResearchRegionFactory)


class ResearchDetailPageResearchTopicRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.ResearchDetailPageResearchTopicRelation

    detail_page = factory.SubFactory(detail_page_factory.ResearchDetailPageFactory)
    topic = factory.SubFactory(taxonomies_factory.ResearchTopicFactory)


class ResearchLandingPageResearchTopicRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.ResearchLandingPageFeaturedResearchTopicRelation

    landing_page = factory.SubFactory(landing_page_factory.ResearchLandingPageFactory)
    topic = factory.SubFactory(taxonomies_factory.ResearchTopicFactory)
