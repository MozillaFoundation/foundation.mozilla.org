import factory
import wagtail_factories

from foundation_cms.legacy_cms.wagtailpages.pagemodels import customblocks


class ImageBlockFactory(wagtail_factories.StructBlockFactory):
    class Meta:
        model = customblocks.ImageBlock

    image = factory.SubFactory(wagtail_factories.ImageChooserBlockFactory)
    altText = factory.Faker("sentence", nb_words=8)
