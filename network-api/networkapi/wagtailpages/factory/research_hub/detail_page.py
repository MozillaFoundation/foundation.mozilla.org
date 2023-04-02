import random

import factory
import wagtail_factories

from networkapi.utility.faker import helpers as faker_helpers
from networkapi.wagtailpages import models as wagtailpage_models
from networkapi.wagtailpages.factory import documents as documents_factory
from networkapi.wagtailpages.factory import image_factory


class ResearchDetailPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = wagtailpage_models.ResearchDetailPage

    title = factory.Faker("text", max_nb_chars=50)
    cover_image = factory.SubFactory(image_factory.ImageFactory)
    research_links = factory.RelatedFactoryList(
        factory="networkapi.wagtailpages.factory.research_hub.detail_page.ResearchDetailLinkFactory",
        factory_related_name="research_detail_page",
        size=lambda: random.randint(1, 2),
        with_url=True,
    )
    original_publication_date = factory.Faker("date_object")
    introduction = factory.Faker("text", max_nb_chars=300)

    @factory.lazy_attribute
    def overview(self):
        faker = faker_helpers.get_faker()
        return "\n\n".join(faker.paragraphs(nb=3))

    @factory.lazy_attribute
    def collaborators(self):
        faker = faker_helpers.get_faker()
        names = []
        for _ in range(random.randint(1, 5)):
            names.append(faker.name())
        return "; ".join(names)

    research_authors = factory.RelatedFactoryList(
        factory="networkapi.wagtailpages.factory.research_hub.relations.ResearchAuthorRelationFactory",
        factory_related_name="research_detail_page",
        size=1,
    )

    related_topics = factory.RelatedFactoryList(
        factory=(
            "networkapi.wagtailpages.factory.research_hub.relations.ResearchDetailPageResearchTopicRelationFactory"
        ),
        factory_related_name="research_detail_page",
        size=1,
    )

    related_regions = factory.RelatedFactoryList(
        factory=(
            "networkapi.wagtailpages.factory.research_hub.relations.ResearchDetailPageResearchRegionRelationFactory"
        ),
        factory_related_name="research_detail_page",
        size=1,
    )


class ResearchDetailLinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.ResearchDetailLink

    label = factory.Faker("text", max_nb_chars=30)
    url = ""
    page = None
    document = None

    class Params:
        with_url = factory.Trait(
            url=factory.Faker("uri"),
        )
        with_page = factory.Trait(page=factory.SubFactory(wagtail_factories.PageFactory))
        with_document = factory.Trait(document=factory.SubFactory(documents_factory.DocumentFactory))
