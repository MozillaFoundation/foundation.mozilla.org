import factory
import wagtail_factories

from networkapi.wagtailpages.pagemodels import customblocks


class LinkButtonBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = customblocks.LinkButtonBlock

    class Params:
        is_relative = False  # Whether this is a relative link or not

    label = factory.Faker("sentence", nb_words=3)
    URL = factory.Maybe("is_relative", yes_declaration=factory.Faker("url"), no_declaration=factory.Faker("uri_path"))
