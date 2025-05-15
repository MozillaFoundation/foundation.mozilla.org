import factory

from foundation_cms.legacy_apps.wagtailpages import models as wagtailpage_models
from foundation_cms.legacy_apps.wagtailpages.factory import profiles as profiles_factory
from foundation_cms.legacy_apps.wagtailpages.factory.libraries.rcc import (
    detail_page as detail_page_factory,
)
from foundation_cms.legacy_apps.wagtailpages.factory.libraries.rcc import (
    landing_page as landing_page_factory,
)
from foundation_cms.legacy_apps.wagtailpages.factory.libraries.rcc import (
    taxonomies as taxonomies_factory,
)


class RCCAuthorRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.RCCAuthorRelation

    detail_page = factory.SubFactory(detail_page_factory.RCCDetailPageFactory)
    author_profile = factory.SubFactory(profiles_factory.ProfileFactory)


class RCCLandingPageFeaturedAuthorsRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.RCCLandingPageFeaturedAuthorsRelation

    landing_page = factory.SubFactory(landing_page_factory.RCCLandingPageFactory)
    author = factory.SubFactory(profiles_factory.ProfileFactory)


class RCCLandingPageFeaturedRCCContentTypeRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.RCCLandingPageFeaturedRCCContentTypeRelation

    landing_page = factory.SubFactory(landing_page_factory.RCCLandingPageFactory)
    content_type = factory.SubFactory(taxonomies_factory.RCCContentTypeFactory)


class RCCDetailPageRCCContentTypeRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.RCCDetailPageRCCContentTypeRelation

    detail_page = factory.SubFactory(detail_page_factory.RCCDetailPageFactory)
    content_type = factory.SubFactory(taxonomies_factory.RCCContentTypeFactory)


class RCCDetailPageRCCTopicRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.RCCDetailPageRCCTopicRelation

    detail_page = factory.SubFactory(detail_page_factory.RCCDetailPageFactory)
    topic = factory.SubFactory(taxonomies_factory.RCCTopicFactory)


class RCCDetailPageRCCCurricularAreaRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.RCCDetailPageRCCCurricularAreaRelation

    detail_page = factory.SubFactory(detail_page_factory.RCCDetailPageFactory)
    curricular_area = factory.SubFactory(taxonomies_factory.RCCCurricularAreaFactory)
