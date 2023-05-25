import factory

from networkapi.wagtailpages import models as wagtailpage_models
from networkapi.wagtailpages.factory import profiles as profiles_factory
from networkapi.wagtailpages.factory.libraries.rcc import (
    detail_page as detail_page_factory,
)
from networkapi.wagtailpages.factory.libraries.rcc import (
    landing_page as landing_page_factory,
)
from networkapi.wagtailpages.factory.libraries.rcc import (
    taxonomies as taxonomies_factory,
)


class RCCAuthorRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.RCCAuthorRelation

    rcc_detail_page = factory.SubFactory(detail_page_factory.RCCDetailPageFactory)
    author_profile = factory.SubFactory(profiles_factory.ProfileFactory)


class RCCLandingPageFeaturedRCCContentTypeRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.RCCLandingPageFeaturedRCCContentTypeRelation

    rcc_landing_page = factory.SubFactory(landing_page_factory.RCCLandingPageFactory)
    content_type = factory.SubFactory(taxonomies_factory.RCCContentTypeFactory)


class RCCDetailPageRCCContentTypeRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.RCCDetailPageRCCContentTypeRelation

    rcc_detail_page = factory.SubFactory(detail_page_factory.RCCDetailPageFactory)
    content_type = factory.SubFactory(taxonomies_factory.RCCContentTypeFactory)


class RCCDetailPageRCCTopicRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.RCCDetailPageRCCTopicRelation

    rcc_detail_page = factory.SubFactory(detail_page_factory.RCCDetailPageFactory)
    rcc_topic = factory.SubFactory(taxonomies_factory.RCCTopicFactory)


class RCCDetailPageRCCCurricularAreaRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.RCCDetailPageRCCCurricularAreaRelation

    rcc_detail_page = factory.SubFactory(detail_page_factory.RCCDetailPageFactory)
    curricular_area = factory.SubFactory(taxonomies_factory.RCCCurricularAreaFactory)
