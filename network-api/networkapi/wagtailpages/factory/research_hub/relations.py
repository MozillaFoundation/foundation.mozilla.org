import factory

from networkapi.wagtailpages import models as wagtailpage_models
from networkapi.wagtailpages.factory import profiles as profiles_factory
from networkapi.wagtailpages.factory.research_hub import detail_page as detail_page_factory, \
    taxonomies as taxonomies_factory, landing_page as landing_page_factory


class ResearchAuthorRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.ResearchAuthorRelation

    research_detail_page = factory.SubFactory(detail_page_factory.ResearchDetailPageFactory)
    author_profile = factory.SubFactory(profiles_factory.ProfileFactory)


class ResearchDetailPageResearchRegionRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.ResearchDetailPageResearchRegionRelation

    research_detail_page = factory.SubFactory(detail_page_factory.ResearchDetailPageFactory)
    research_region = factory.SubFactory(taxonomies_factory.ResearchRegionFactory)


class ResearchDetailPageResearchTopicRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.ResearchDetailPageResearchTopicRelation

    research_detail_page = factory.SubFactory(detail_page_factory.ResearchDetailPageFactory)
    research_topic = factory.SubFactory(taxonomies_factory.ResearchTopicFactory)


class ResearchLandingPageResearchTopicRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.ResearchLandingPageFeaturedResearchTopicRelation

    research_landing_page = factory.SubFactory(landing_page_factory.ResearchLandingPageFactory)
    research_topic = factory.SubFactory(taxonomies_factory.ResearchTopicFactory)
