import random

import factory

from foundation_cms.legacy_cms.wagtailpages import models as wagtailpage_models
from foundation_cms.legacy_cms.wagtailpages.factory.libraries import (
    detail_page as library_detail_page_factories,
)


class ResearchDetailPageFactory(library_detail_page_factories.LibraryDetailPageAbstractFactory):
    class Meta:
        model = wagtailpage_models.ResearchDetailPage

    links = factory.RelatedFactoryList(
        factory="foundation_cms.legacy_cms.wagtailpages.factory.libraries.research_hub.detail_page.ResearchDetailLinkFactory",
        factory_related_name="detail_page",
        size=lambda: random.randint(1, 2),
        with_url=True,
    )

    authors = factory.RelatedFactoryList(
        factory="foundation_cms.legacy_cms.wagtailpages.factory.libraries.research_hub.relations.ResearchAuthorRelationFactory",
        factory_related_name="detail_page",
        size=1,
    )

    related_topics = factory.RelatedFactoryList(
        factory=(
            "foundation_cms.legacy_cms.wagtailpages.factory.libraries.research_hub"
            ".relations.ResearchDetailPageResearchTopicRelationFactory"
        ),
        factory_related_name="detail_page",
        size=1,
    )

    related_regions = factory.RelatedFactoryList(
        factory=(
            "foundation_cms.legacy_cms.wagtailpages.factory.libraries.research_hub"
            ".relations.ResearchDetailPageResearchRegionRelationFactory"
        ),
        factory_related_name="detail_page",
        size=1,
    )


class ResearchDetailLinkFactory(library_detail_page_factories.LibraryDetailLinkBaseAbstractFactory):
    class Meta:
        model = wagtailpage_models.ResearchDetailLink
