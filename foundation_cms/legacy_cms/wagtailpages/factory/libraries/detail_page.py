import random

import factory
import wagtail_factories

from legacy_cms.utility.faker import helpers as faker_helpers
from legacy_cms.wagtailpages import models as wagtailpage_models
from legacy_cms.wagtailpages.factory import documents as documents_factory
from legacy_cms.wagtailpages.factory import image_factory


class LibraryDetailPageAbstractFactory(wagtail_factories.PageFactory):
    class Meta:
        model = wagtailpage_models.LibraryDetailPage
        abstract = True

    title = factory.Faker("text", max_nb_chars=50)
    cover_image = factory.SubFactory(image_factory.ImageFactory)

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


class LibraryDetailLinkBaseAbstractFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = wagtailpage_models.LibraryDetailLinkBase
        abstract = True

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
