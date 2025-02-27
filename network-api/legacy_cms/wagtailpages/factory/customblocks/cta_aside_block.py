import factory
import wagtail_factories

from legacy_cms.wagtailpages.pagemodels import customblocks


class CTAAsideBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = customblocks.CTAAsideBlock

    title = factory.Faker("sentence", nb_words=4)
    body = factory.Faker("sentence", nb_words=10)
    button = factory.SubFactory(
        "legacy_cms.wagtailpages.factory.customblocks.link_button_block.LinkButtonBlockFactory",
        styling="btn-secondary",
    )
