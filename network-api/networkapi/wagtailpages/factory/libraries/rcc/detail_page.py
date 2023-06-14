import random

import factory
import wagtail_factories

from networkapi.utility.faker import helpers as faker_helpers
from networkapi.wagtailpages import models as wagtailpage_models
from networkapi.wagtailpages.factory import documents as documents_factory
from networkapi.wagtailpages.factory import image_factory


class RCCDetailPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = wagtailpage_models.RCCDetailPage

    title = factory.Faker("text", max_nb_chars=50)
    cover_image = factory.SubFactory(image_factory.ImageFactory)
    links = factory.RelatedFactoryList(
        factory="networkapi.wagtailpages.factory.libraries.rcc.detail_page.RCCDetailLinkFactory",
        factory_related_name="detail_page",
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

    authors = factory.RelatedFactoryList(
        factory="networkapi.wagtailpages.factory.libraries.rcc.relations.RCCAuthorRelationFactory",
        factory_related_name="detail_page",
        size=1,
    )

    related_content_types = factory.RelatedFactoryList(
        factory="networkapi.wagtailpages.factory.libraries.rcc.relations.RCCDetailPageRCCContentTypeRelationFactory",
        factory_related_name="detail_page",
        size=1,
    )

    related_curricular_areas = factory.RelatedFactoryList(
        factory=(
            "networkapi.wagtailpages.factory.libraries.rcc.relations.RCCDetailPageRCCCurricularAreaRelationFactory"
        ),
        factory_related_name="detail_page",
        size=1,
    )

    related_topics = factory.RelatedFactoryList(
        factory="networkapi.wagtailpages.factory.libraries.rcc.relations.RCCDetailPageRCCTopicRelationFactory",
        factory_related_name="detail_page",
        size=1,
    )


class RCCDetailLinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.RCCDetailLink

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
