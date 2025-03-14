import factory
import wagtail_factories

from foundation_cms.legacy_apps.wagtailpages.pagemodels import customblocks


class CTAAsideBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = customblocks.CTAAsideBlock

    title = factory.Faker("sentence", nb_words=4)
    body = factory.Faker("sentence", nb_words=10)
    button = factory.SubFactory(
        "foundation_cms.legacy_apps.wagtailpages.factory.customblocks.link_button_block.LinkButtonBlockFactory",
        styling="btn-secondary",
    )
