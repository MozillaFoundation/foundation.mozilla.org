import random

import factory

from foundation_cms.legacy_apps.wagtailpages import models as wagtailpage_models
from foundation_cms.legacy_apps.wagtailpages.factory.libraries import (
    detail_page as library_detail_page_factories,
)


class RCCDetailPageFactory(library_detail_page_factories.LibraryDetailPageAbstractFactory):
    class Meta:
        model = wagtailpage_models.RCCDetailPage

    links = factory.RelatedFactoryList(
        factory=("foundation_cms.legacy_apps.wagtailpages.factory.libraries" ".rcc.detail_page.RCCDetailLinkFactory"),
        factory_related_name="detail_page",
        size=lambda: random.randint(1, 2),
        with_url=True,
    )

    authors = factory.RelatedFactoryList(
        factory=(
            "foundation_cms.legacy_apps.wagtailpages.factory.libraries" ".rcc.relations.RCCAuthorRelationFactory"
        ),
        factory_related_name="detail_page",
        size=1,
    )

    related_content_types = factory.RelatedFactoryList(
        factory=(
            "foundation_cms.legacy_apps.wagtailpages.factory.libraries"
            ".rcc.relations.RCCDetailPageRCCContentTypeRelationFactory"
        ),
        factory_related_name="detail_page",
        size=1,
    )

    related_curricular_areas = factory.RelatedFactoryList(
        factory=(
            "foundation_cms.legacy_apps.wagtailpages.factory.libraries"
            ".rcc.relations.RCCDetailPageRCCCurricularAreaRelationFactory"
        ),
        factory_related_name="detail_page",
        size=1,
    )

    related_topics = factory.RelatedFactoryList(
        factory=(
            "foundation_cms.legacy_apps.wagtailpages.factory.libraries"
            ".rcc.relations.RCCDetailPageRCCTopicRelationFactory"
        ),
        factory_related_name="detail_page",
        size=1,
    )


class RCCDetailLinkFactory(library_detail_page_factories.LibraryDetailLinkBaseAbstractFactory):
    class Meta:
        model = wagtailpage_models.RCCDetailLink
